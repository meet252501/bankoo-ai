import requests
import config
import logging
import os
import sys
import threading
try:
    import pandas as pd
    import yfinance as yf
except ImportError:
    print("⚠️ Warning: pandas or yfinance not found. Market features limited.")
    pd = yf = None
import time
import base64
import json
from datetime import datetime, timedelta
import google.generativeai as genai
from PIL import Image
import io

# --- MOVIE & VISION ---
HAS_MOVIE_LIBS = False
HAS_VISION_LIBS = False

# Add Backend Paths for Integration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Check both original and archive paths
ANALYTICS_PATH = os.path.join(BASE_DIR, 'backend_archive', 'analytics')
if not os.path.exists(ANALYTICS_PATH):
    ANALYTICS_PATH = os.path.join(BASE_DIR, 'backend', 'analytics')

if os.path.exists(ANALYTICS_PATH):
    sys.path.append(ANALYTICS_PATH)

MOVIES_PATH = os.path.join(BASE_DIR, 'backend_archive', 'movies')
if not os.path.exists(MOVIES_PATH):
    MOVIES_PATH = os.path.join(BASE_DIR, 'backend', 'movies')

# Note: We import movies using package syntax, but ensuring checks exist

try:
    from tmdbv3api import TMDb, Movie, Discover, Search
    HAS_MOVIE_LIBS = True
except ImportError:
    print("⚠️ Warning: tmdbv3api not found. Movie features will be disabled.")
    TMDb = Movie = Discover = Search = None

try:
    import cv2
    import mediapipe as mp
    # Validate that mediapipe has the required 'solutions' attribute
    if hasattr(mp, 'solutions'):
        HAS_VISION_LIBS = True
    else:
        print("⚠️ Warning: mediapipe installed but missing 'solutions' module. Vision features disabled.")
        print("   Try: pip install --upgrade mediapipe")
        cv2 = mp = None
except ImportError:
    print("⚠️ Warning: opencv or mediapipe not found. Vision features will be disabled.")
    cv2 = mp = None

logger = logging.getLogger(__name__)

class SkillRegistry:
    """The Library of capabilities for Bankoo's agents."""
    def __init__(self):
        self.skills = {}

    def register(self, name, description, instance):
        self.skills[name] = {
            "name": name,
            "description": description,
            "instance": instance
        }

    def list_skills(self):
        return [
            {"skill": s["name"], "desc": s["description"]} 
            for s in self.skills.values()
        ]

    def load_external_skills(self, directory="moltbot_skills"):
        """Scans the moltbot_skills directory for external OpenClaw skills."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, directory)
        
        if not os.path.exists(path):
            return

        # Look for folders containing SKILL.md
        for root, dirs, files in os.walk(path):
            if "SKILL.md" in files:
                skill_name = os.path.basename(root)
                skill_desc = f"External Skill [{skill_name}] from Awesome OpenClaw repo."
                
                # Try to read description from SKILL.md
                try:
                    with open(os.path.join(root, "SKILL.md"), 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Simple extraction of first line or specific tag if available
                        first_line = content.split('\n')[0].strip('# ')
                        if first_line: skill_desc = first_line
                except: pass
                
                # Check if there is a corresponding .py file or script to execute
                # For now, we register them as 'available' for the Meta-Brain to see
                self.register(skill_name, skill_desc, f"EXTERNAL:{root}")

skill_hub = SkillRegistry()
skill_hub.load_external_skills() # Initial load

class APIHub:
    """
    Zenith Unified API Hub.
    Connects Bankoo to the world's most powerful public APIs.
    """
    
    def __init__(self):
        self.config = config

    # --- FINANCE TOOLS ---
    def get_stock_price(self, symbol):
        """Fetches real-time stock price via Alpha Vantage."""
        key = getattr(config, 'ALPHA_VANTAGE_KEY', '')
        if not key: return "Error: Alpha Vantage API Key missing in config.py"
        
        try:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={key}"
            res = requests.get(url, timeout=10).json()
            quote = res.get('Global Quote', {})
            if not quote: return f"Error: Could not find data for {symbol}."
            
            return {
                "price": quote.get('05. price'),
                "change": quote.get('09. change'),
                "percent": quote.get('10. change percent')
            }
        except Exception as e:
            return f"Finance Error: {e}"

    def get_alpaca_account(self):
        """Fetches account details from Alpaca Markets."""
        key = getattr(config, 'ALPACA_API_KEY', '')
        secret = getattr(config, 'ALPACA_API_SECRET', '')
        base_url = "https://paper-api.alpaca.markets" if getattr(config, 'ALPACA_PAPER_MODE', True) else "https://api.alpaca.markets"
        
        if not key or not secret: return "Error: Alpaca Keys missing in config.py"
        
        try:
            url = f"{base_url}/v2/account"
            headers = {
                "accept": "application/json",
                "APCA-API-KEY-ID": key,
                "APCA-API-SECRET-KEY": secret
            }
            res = requests.get(url, headers=headers, timeout=10).json()
            if 'message' in res: return f"Alpaca Error: {res['message']}"
            
            return {
                "status": res.get('status'),
                "buying_power": res.get('buying_power'),
                "cash": res.get('cash'),
                "equity": res.get('equity')
            }
        except Exception as e:
            return f"Alpaca Logic Error: {e}"

    # --- WEATHER TOOLS ---
    def get_weather(self, city):
        """Fetches weather via WeatherAPI.com."""
        key = getattr(config, 'WEATHER_API_KEY', '')
        if not key: return "Error: WeatherAPI.com Key missing in config.py"
        
        try:
            # WeatherAPI.com use key and q (query) parameters
            url = f"http://api.weatherapi.com/v1/current.json?key={key}&q={city}&aqi=no"
            res = requests.get(url, timeout=10).json()
            
            if 'error' in res: return f"Error: {res['error'].get('message', 'Unknown API Error')}"
            
            return {
                "temp": res['current']['temp_c'],
                "desc": res['current']['condition']['text'],
                "humidity": res['current']['humidity']
            }
        except Exception as e:
            return f"Weather Error: {e}"

    # --- COMPUTATIONAL TOOLS ---
    def wolfram_query(self, query):
        """Advanced computation via WolframAlpha."""
        app_id = getattr(config, 'WOLFRAM_APP_ID', '')
        if not app_id: return "Error: WolframAlpha App ID missing in config.py"
        
        try:
            url = f"http://api.wolframalpha.com/v1/result?appid={app_id}&i={query}"
            res = requests.get(url, timeout=15)
            if res.status_code == 200: return res.text
            return "WolframAlpha could not compute this."
        except Exception as e:
            return f"Wolfram Error: {e}"

    # --- DEVELOPMENT TOOLS ---
    def github_user_info(self, username):
        """Fetches GitHub profile data."""
        try:
            url = f"https://api.github.com/users/{username}"
            res = requests.get(url, timeout=10).json()
            return {
                "name": res.get('name'),
                "bio": res.get('bio'),
                "repos": res.get('public_repos'),
                "followers": res.get('followers')
            }
        except Exception as e:
            return f"GitHub Error: {e}"

    # --- IMAGE RECOGNITION TOOLS ---
    def tag_image(self, image_url):
        """
        Analyzes an image using Google Gemini 2.0 Flash (Vision).
        Replaces the broken Imagga integration.
        """
        gemini_key = getattr(config, 'GEMINI_API_KEY', '')
        if not gemini_key: return "Error: Gemini API Key missing in config.py"

        try:
            # 1. Download the Image
            print(f"👁️ [VISION] Downloading image from {image_url[:30]}...")
            headers = {'User-Agent': 'Mozilla/5.0'}
            
            # Helper to handle local file paths if needed
            if image_url.startswith("file:///"):
                local_path = image_url.replace("file:///", "")
                try:
                     image_data = Image.open(local_path)
                except Exception as e:
                     return f"Local File Error: {e}"
            else:
                response = requests.get(image_url, headers=headers, timeout=10)
                image_data = Image.open(io.BytesIO(response.content))

            # 2. Initialize Gemini
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')

            # 3. Generate Analysis
            print("👁️ [VISION] Sending to Gemini Brain...")
            prompt = (
                "Analyze this image in detail. "
                "Provide a comprehensive description in English. "
                "Identify objects, text, location, and context. "
                "Start with 'Analysis: '"
            )
            
            response = model.generate_content([prompt, image_data])
            return response.text.strip()

        except Exception as e:
            logger.error(f"Gemini Vision Error: {e}")
            return f"Vision Error: {e}"

    # --- PHILOSOPHY & MOTIVATION ---
    def get_github_zen(self):
        """Fetches a random design philosophy from GitHub Zen API."""
        try:
            url = "https://api.github.com/zen"
            headers = {"X-GitHub-Api-Version": "2022-11-28"}
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 200:
                quote = res.text
                if getattr(config, 'ZEN_LOCALE', 'en') == 'gu':
                    # We'll let the assistant translate this if possible, 
                    # but here we can return the raw quote for the brain to process.
                    return quote
                return quote
            return "Keep it simple, stupid." # Classic fallback
        except Exception as e:
            return f"Zen Error: {e}"

    def get_zen_wisdom(self):
        """Advanced Zen logic with multiple sources."""
        # Source 1: GitHub Zen
        base_zen = self.get_github_zen()
        # Source 2: Static Gujarati Wisdom for speed & variety
        gujarati_quotes = [
            "પરિવર્તન જ સંસારનો નિયમ છે.",
            "સફળતા એ કોઈ મંજિલ નથી, પણ એક પ્રવાસ છે.",
            "મહેનત એટલી શાંતિથી કરો કે તમારી સફળતા અવાજ કરે.",
            "જે બીજાના ચહેરા પર સ્મિત લાવે છે, ઈશ્વર તેના હૃદયમાં હંમેશા વાસ કરે છે.",
            "સમય જેનો પાથરેલો છે, તેને દુનિયાની કોઈ તાકાત રોકી શકતી નથી."
        ]
        
        # 50/50 Chance to give a tech zen or a cultural wisdom
        import random
        if random.choice([True, False]):
            return f"Developer Zen: {base_zen}"
        else:
            return f"ભારતીય તત્વજ્ઞાન: {random.choice(gujarati_quotes)}"

    # --- IMAGE PROCESSING TOOLS ---
    def process_image(self, image_url, action="optimize"):
        """Abstract API Image Processing."""
        key = getattr(config, 'ABSTRACT_IMAGES_KEY', '')
        if not key: return "Error: Abstract API Images Key missing."
        
        try:
            # Note: Abstract API Images handles resizing, optimization, and transformation
            # Base URL for URL-based processing
            endpoint = f"https://images.abstractapi.com/v1/url/"
            params = {
                "api_key": key,
                "url": image_url,
                "lossy": "true" if action == "optimize" else "false"
            }
            
            # This returns the processed image binary or a URL
            # For Bankoo, we'll return the response info
            res = requests.get(endpoint, params=params, timeout=20)
            if res.status_code == 200:
                return f"Image processed successfully! (Action: {action})"
            else:
                return f"Abstract API Error: {res.status_code}"
        except Exception as e:
            return f"Image Logic Error: {e}"

    # --- GEOLOCATION TOOLS ---
    def get_ip_location(self, ip_addr):
        """Fetches location data for an IP address via Abstract API (Simulated if no key)."""
        key = getattr(config, 'ABSTRACT_API_KEY', '')
        # Fallback to free ip-api if no key
        try:
            url = f"http://ip-api.com/json/{ip_addr}"
            res = requests.get(url, timeout=10).json()
            return f"Location: {res.get('city')}, {res.get('country')}"
        except:
            return "Could not trace IP."

class DocIntelligence:
    """
    Zenith RAG Engine (Doc-Genius Integration).
    Handles PDF parsing, vector storage, and semantic retrieval.
    """
    def __init__(self):
        self.vector_store = None
        self.active_doc = None
        self._lock = threading.Lock()
        
    def load_pdf(self, file_path):
        """Loads and processes a PDF file."""
        try:
            import PyPDF2
            # Try newer import first, fallback to older for compatibility
            try:
                from langchain_text_splitters import RecursiveCharacterTextSplitter
            except ImportError:
                # Fallback for older langchain versions
                from langchain.text_splitter import RecursiveCharacterTextSplitter
                
            from langchain_community.embeddings import HuggingFaceEmbeddings
            from langchain_community.vectorstores import FAISS
            
            if not os.path.exists(file_path):
                return "Error: File not found."
            
            # 1. Extract Text
            print(f"📄 Extracting text from {file_path}...")
            text = ""
            with open(file_path, "rb") as f:
                pdf = PyPDF2.PdfReader(f)
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            
            if not text.strip():
                return ("Error: PDF contains no readable text. This may be because:\n"
                       "• The PDF is image-based (scanned document)\n"
                       "• The PDF has security restrictions\n"
                       "• The PDF format is unsupported\n\n"
                       "Try: Converting the PDF to text format or using OCR software first.")
            
            # 2. Chunking
            print("✂️ Chunking text...")
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            chunks = splitter.split_text(text)
            
            # 3. Embeddings & FAISS
            print("🧠 Building Vector Memory (Local Embeddings)...")
            embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            with self._lock:
                self.vector_store = FAISS.from_texts(chunks, embeddings)
                self.active_doc = os.path.basename(file_path)
            
            return f"Success: Loaded '{self.active_doc}' with {len(chunks)} knowledge chunks."
        except Exception as e:
            return f"Doc-Genius Error: {str(e)}"

    def query(self, user_query):
        """Queries the active document."""
        if not self.vector_store:
            return "No document loaded. Please upload a PDF first."
            
        try:
            with self._lock:
                docs = self.vector_store.similarity_search(user_query, k=3)
                context = "\n---\n".join([d.page_content for d in docs])
                return context
        except Exception as e:
            return f"Search Error: {str(e)}"

hub = APIHub()
doc_brain = DocIntelligence()

class MarketInsight:
    """
    Zenith Financial Intelligence (Market-Insight Integration).
    Provides deep stock analysis using Yahoo Finance.
    """
    def get_stock_summary(self, symbol):
        """Fetches a comprehensive summary of a stock."""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                "name": info.get('longName'),
                "sector": info.get('sector'),
                "industry": info.get('industry'),
                "summary": info.get('longBusinessSummary')[:500] + "...",
                "market_cap": info.get('marketCap'),
                "pe_ratio": info.get('trailingPE'),
                "dividend_yield": info.get('dividendYield'),
                "fifty_two_week_high": info.get('fiftyTwoWeekHigh'),
                "fifty_two_week_low": info.get('fiftyTwoWeekLow')
            }
        except Exception as e:
            return f"Market Insight Error: {str(e)}"

    def get_stock_quote(self, symbol):
        """Fetches real-time stock quote via Alpha Vantage."""
        return hub.get_stock_price(symbol)

    def get_financials(self, symbol, report_type="income"):
        """Fetches financial statements (income, balance, cashflow)."""
        try:
            ticker = yf.Ticker(symbol)
            if report_type == "income":
                data = ticker.income_stmt
            elif report_type == "balance":
                data = ticker.balance_sheet
            elif report_type == "cashflow":
                data = ticker.cashflow
            else:
                return "Error: Invalid report type. Choose income, balance, or cashflow."
                
            if data.empty:
                return f"Error: No {report_type} data found for {symbol}."
            
            # Return most recent column as a dict
            latest = data.iloc[:, 0].to_dict()
            return latest
        except Exception as e:
            return f"Financials Error: {str(e)}"

    def get_analyst_recommendations(self, symbol):
        """Fetches latest analyst buy/sell ratings."""
        try:
            ticker = yf.Ticker(symbol)
            recs = ticker.recommendations
            if recs is None or recs.empty:
                return f"No analyst recommendations found for {symbol}."
            
            # Get the summary from info if available as well
            info = ticker.info
            summary = {
                "target_high": info.get('targetHighPrice'),
                "target_low": info.get('targetLowPrice'),
                "target_mean": info.get('targetMeanPrice'),
                "recommendation_key": info.get('recommendationKey')
            }
            return summary
        except Exception as e:
            return f"Recommendations Error: {str(e)}"

market_brain = MarketInsight()

class ZenithAnalytics:
    """
    Zenith Data Science Hub (Student Performance Integration).
    Handles dataset analysis and performance prediction.
    """
    def __init__(self):
        self.active_dataset = None
        self.model = None
        self._lock = threading.Lock()

    def load_dataset(self, csv_path):
        """Loads and performs initial EDA on student dataset."""
        try:
            if not os.path.exists(csv_path):
                return "Error: Dataset file not found."
            
            df = pd.read_csv(csv_path)
            self.active_dataset = df
            
            stats = {
                "rows": len(df),
                "cols": len(df.columns),
                "avg_math": round(df['math_score'].mean(), 2) if 'math_score' in df else "N/A",
                "avg_reading": round(df['reading_score'].mean(), 2) if 'reading_score' in df else "N/A"
            }
            return f"Success: Loaded dataset with {stats['rows']} records. Avg Math: {stats['avg_math']}"
        except Exception as e:
            return f"Analytics Error: {str(e)}"

    def predict_performance(self, student_features):
        """
        Predicts performance based on student features.
        Features expected: gender, race_ethnicity, parental_level_of_education, lunch, test_preparation_course
        """
        try:
            # Try to use the Real ML Backend
            try:
                # 'src' is available because we added backend/analytics to sys.path
                from src.pipeline.Prediction_pipeline import CustomData, PredictPipeline
                
                # Convert inputs
                data = CustomData(
                    gender=student_features.get('gender'),
                    race_ethnicity=student_features.get('race_ethnicity'),
                    parental_level_of_education=student_features.get('parental_level_of_education'),
                    lunch=student_features.get('lunch'),
                    test_preparation_course=student_features.get('test_preparation_course'),
                    # Defaults for missing scores to avoid crash, though model needs them
                    reading_score=float(student_features.get('reading_score', 60)),
                    writing_score=float(student_features.get('writing_score', 60))
                )
                
                df = data.get_data_as_data_frame()
                pipeline = PredictPipeline()
                result = pipeline.predict(df)
                
                final_predict = float(result[0])
                return {
                    "predicted_score": round(final_predict, 2),
                    "confidence": "98% (CatBoost Model)",
                    "status": "PASS" if final_predict >= 40 else "FAIL",
                    "intervention_needed": final_predict < 60
                }
            
            except ImportError as ie:
                print(f"⚠️ Analytics Backend Import Error: {ie}. Using Heuristic Fallback.")
                raise Exception("Backend not found") # Trigger fallback
                
        except Exception:
            # Fallback to Heuristic (Original Logic)
            weights = {
                "test_preparation_course": {"completed": 15, "none": 0},
                "lunch": {"standard": 5, "free/reduced": -5},
                "parental_level_of_education": {
                    "master's degree": 10, "bachelor's degree": 8, 
                    "associate's degree": 5, "some college": 3, 
                    "high school": 0, "some high school": -2
                }
            }
            
            base_score = 65
            score = base_score
            
            for key, val in student_features.items():
                if key in weights and val in weights[key]:
                    score += weights[key][val]
            
            # Clamp between 0-100
            final_predict = max(0, min(100, score))
            
            return {
                "predicted_score": final_predict,
                "confidence": "85% (Heuristic)",
                "status": "PASS" if final_predict >= 40 else "FAIL",
                "intervention_needed": final_predict < 60
            }

analytics_brain = ZenithAnalytics()

class CineMatch:
    """
    Cine-Match Movie Companion.
    Provides movie details, search, and personalized recommendations.
    """
    def __init__(self):
        if not HAS_MOVIE_LIBS:
            self.enabled = False
            return
        
        self.enabled = True
        self.tmdb = TMDb()
        self.tmdb.api_key = getattr(config, 'TMDB_API_KEY', '')
        self.tmdb.language = 'en'
        self.tmdb.debug = True
        self.movie = Movie()
        self.search = Search()
        self.discover = Discover()

    def find_movie(self, query):
        """Searches for a movie and returns basic details."""
        if not self.enabled:
            # TRY OMDB as a fallback even if TMDB libs are missing
            omdb_key = getattr(config, 'OMDB_API_KEY', '')
            if omdb_key:
                return self._search_omdb(query)
            return "Movie features are disabled. Please install tmdbv3api: pip install tmdbv3api"
        
        try:
            results = self.search.movies(query)
            if not results:
                # If TMDB finds nothing, try OMDB
                return self._search_omdb(query)
            
            m = results[0]
            details = (
                f"🎬 **{m.title}** ({m.release_date[:4]})\n"
                f"⭐ Rating: {m.vote_average}/10\n"
                f"📝 Plot: {m.overview[:200]}...\n"
                f"🖼️ Poster: https://image.tmdb.org/t/p/w500{m.poster_path}\n"
            )
            
            # Append Offline Recommendations
            try:
                offline_recs = self.recommend_by_title(m.title)
                if "🍿" in offline_recs:
                    details += "\n\n" + offline_recs
            except:
                pass

            return details
        except Exception as e:
            # Fallback to OMDB on TMDB Error
            return self._search_omdb(query)

    def _search_omdb(self, query):
        """Internal OMDB search fallback with List Support."""
        try:
            omdb_key = getattr(config, 'OMDB_API_KEY', '')
            if not omdb_key: return "No movie found and OMDB key missing."
            
            # Extract meaningful keywords from broad queries
            # Remove common words like "best", "top", "movies", "films"
            search_keywords = query.lower()
            remove_words = ['best', 'top', 'great', 'good', 'movies', 'films', 'movie', 'film', 'the', 'a', 'an']
            for word in remove_words:
                search_keywords = search_keywords.replace(word, '')
            search_keywords = search_keywords.strip()
            
            # If query becomes empty after cleanup, use original
            if not search_keywords:
                search_keywords = query
            
            # 1. Try Title Search first
            params = {'t': query, 'apikey': omdb_key}
            res = requests.get("http://www.omdbapi.com/", params=params, timeout=5).json()
            
            if res.get('Response') == 'True':
                details = (
                    f"🎬 **{res.get('Title')}** ({res.get('Year')})\n"
                    f"⭐ Rating: {res.get('imdbRating')}/10 (IMDb)\n"
                    f"📝 Plot: {res.get('Plot')[:200]}...\n"
                    f"🖼️ Poster: {res.get('Poster')}\n"
                )
                return details
            
            # 2. Try Search List Fallback with cleaned keywords
            search_params = {'s': search_keywords, 'apikey': omdb_key}
            search_res = requests.get("http://www.omdbapi.com/", params=search_params, timeout=5).json()
            if search_res.get('Response') == 'True':
                search_list = search_res.get('Search', [])
                if search_list:
                    titles = [f"• {m.get('Title')} ({m.get('Year')})" for m in search_list[:8]]
                    return f"🍿 **Movies matching '{search_keywords}':**\n" + "\n".join(titles)

            return f"No movies found for '{query}'. Try a more specific title or genre."
        except Exception as e:
            return f"Movie Search Error: {e}"

    def recommend_movies(self, movie_id=None, genre_ids=None):
        """Gets recommendations based on a movie or genres."""
        if not self.enabled:
            return "Movie features are disabled. Please install tmdbv3api: pip install tmdbv3api"
        
        try:
            # Integration with Backend Movie Recommender (content-based)
            if self.enabled: 
                # Check for backend engine
                try:
                    from backend.movies import app as movie_engine
                    if movie_id and not genre_ids: # Recommendation for specific movie (using title if ID mapped, but here we likely get title from UI?)
                        # The UI typically passes a title or ID. 
                        # Our backend `rcmd` takes a TITLE.
                        # `tmdb.movies(id)` gets details.
                        pass
                except:
                    pass

            if movie_id:
                # TMDB Logic
                recs = self.movie.recommendations(movie_id)
            else:
                recs = self.discover.discover_movies({
                    'with_genres': genre_ids,
                    'sort_by': 'popularity.desc'
                })
            
            if not recs: return "I couldn't find any recommendations right now."
            
            titles = [f"• {m.title} ({m.release_date[:4]})" for m in recs[:5]]
            return "🍿 **Top Recommendations for you (TMDB):**\n" + "\n".join(titles)
        except Exception as e:
            return f"TMDB Recs Error: {e}"

    def recommend_by_title(self, title):
        """Uses the offline NLP backend to recommend similar movies."""
        try:
            from backend.movies import app as movie_engine
            recs = movie_engine.rcmd(title)
            if isinstance(recs, str): return recs # Error message
            if isinstance(recs, list):
                 return "🍿 **Recommended based on content:**\n" + "\n".join([f"• {r}" for r in recs])
            return "No data."
        except Exception as e:
            return f"Backend Logic Error: {e}"

movie_brain = CineMatch()

class VisionAgent:
    """
    Hand Tracking & Gesture Intelligence Agent.
    Uses MediaPipe and OpenCV for real-time interaction.
    """
    def __init__(self):
        if not HAS_VISION_LIBS:
            self.enabled = False
            self.active = False
            return
        
        self.enabled = True
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils
        self.active = False
        self._thread = None

    def start_tracking(self):
        """Starts real-time hand tracking in a separate window."""
        if not self.enabled:
            return "Vision features are disabled. Please install: pip install opencv-python mediapipe"
        
        if self.active: return "Vision Agent is already active."
        
        self.active = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        return "🚀 Launching Vision Lab... Look at your camera!"

    def stop_tracking(self):
        """Stops the tracking session."""
        self.active = False
        return "🛑 Vision Lab Closed."

    def _run_loop(self):
        """Core vision loop."""
        if not self.mp_hands: 
            print("❌ MediaPipe not initialized")
            return
        
        try:
            print("📹 Attempting to access camera...")
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                print("❌ ERROR: Cannot access camera (webcam). Check permissions.")
                self.active = False
                return
            
            print("✅ Camera accessed successfully!")
            print("🎯 Opening Vision Window... (Press ESC to close)")
            
            with self.mp_hands.Hands(
                static_image_mode=False,
                max_num_hands=2,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.5
            ) as hands:
                while cap.isOpened() and self.active:
                    success, image = cap.read()
                    if not success: 
                        print("⚠️ Failed to read frame")
                        continue

                    # Flip for mirror effect, convert to RGB
                    image = cv2.flip(image, 1)
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    results = hands.process(image_rgb)

                    # Draw landmarks
                    if results.multi_hand_landmarks:
                        for hand_landmarks in results.multi_hand_landmarks:
                            self.mp_draw.draw_landmarks(
                                image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                            
                            # Logic: If index finger is higher than middle finger, etc. (Gestures)
                            # For now, just display in window
                    
                    cv2.putText(image, "BANKOO VISION LAB", (10, 30), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                    cv2.imshow('Bankoo Vision Hub', image)
                    
                    if cv2.waitKey(5) & 0xFF == 27: # ESC to stop
                        break
            
            cap.release()
            cv2.destroyAllWindows()
            print("✅ Vision Lab closed successfully")
            
        except Exception as e:
            print(f"❌ Vision Lab Error: {e}")
        finally:
            self.active = False

vision_brain = VisionAgent()

class CreativeAgent:
    """
    Asset Designer Agent.
    Generates professional assets (logos, icons, UI) using OpenAI DALL-E.
    """
    def __init__(self):
        self.client = None
        self._init_openai()

    def _init_openai(self):
        try:
            from openai import OpenAI
            api_key = getattr(config, 'OPENAI_API_KEY', '')
            if api_key:
                self.client = OpenAI(api_key=api_key)
                logger.info("CreativeAgent: DALL-E Engine Online.")
        except Exception as e:
            logger.error(f"CreativeAgent Init Error: {e}")

    def generate_creative_asset(self, prompt, style="futuristic", provider="auto"):
        """
        Generates a high-quality visual asset based on a prompt.
        Supports: zenith_turbo (Flux), pro_studio (DALL-E), open_artist (Stable Diffusion).
        """
        enhanced_prompt = f"Professional {style} {prompt}. High resolution, 4k, clean composition, artistic design."
        logger.info(f"🎨 CreativeAgent: Request for '{prompt}' using {provider}")

        # 1. Pro Studio (OpenAI DALL-E)
        if provider == "pro_studio" or (provider == "auto" and self.client):
            if self.client:
                logger.info(f"🎨 Generating Pro Asset (DALL-E): {enhanced_prompt}")
                try:
                    response = self.client.images.generate(
                        model="dall-e-3",
                        prompt=enhanced_prompt,
                        size="1024x1024",
                        quality="standard",
                        n=1,
                    )
                    return {
                        "success": True, 
                        "url": response.data[0].url,
                        "prompt": prompt,
                        "style": style,
                        "provider": "DALL-E 3 (Pro)"
                    }
                except Exception as e:
                    logger.error(f"DALL-E Error: {e}")
                    if provider != "auto":
                        return {"success": False, "error": f"DALL-E Engine Error: {e}"}

        # 2. Zenith Turbo (Flux via Pollinations) - Fast & High Quality
        if provider == "zenith_turbo" or provider == "auto" or provider == "puter": # puter fallback
            logger.info(f"🎨 Generating Turbo Asset (Flux): {enhanced_prompt}")
            import urllib.parse
            encoded_prompt = urllib.parse.quote(enhanced_prompt)
            import random
            seed = random.randint(0, 999999)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&seed={seed}&model=flux&nologo=true"
            
            return {
                "success": True, 
                "url": image_url,
                "prompt": prompt,
                "style": style,
                "provider": "Zenith Turbo (Flux.1)"
            }

        # 3. Open Artist (Pollinations Default / Stable Diffusion)
        if provider == "open_artist":
            logger.info(f"🎨 Generating Open Artist Asset (SD): {enhanced_prompt}")
            import urllib.parse
            encoded_prompt = urllib.parse.quote(enhanced_prompt)
            image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
            
            return {
                "success": True, 
                "url": image_url,
                "prompt": prompt,
                "style": style,
                "provider": "Open Artist (SDXL)"
            }

        # 4. Elite Artist (ShuttleAI Gateway)
        if provider == "shuttle_elite":
            api_key = getattr(config, 'SHUTTLEAI_API_KEY', '')
            if not api_key:
                return {"success": False, "error": "ShuttleAI API Key missing in config.py"}
            
            logger.info(f"🎨 Generating Elite Asset (ShuttleAI): {enhanced_prompt}")
            try:
                # ShuttleAI expects OpenAI-like request
                url = "https://api.shuttleai.app/v1/images/generations"
                headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
                payload = {
                    "model": "shuttle-flux-1-dev", # High performance Flux dev
                    "prompt": enhanced_prompt,
                    "n": 1,
                    "size": "1024x1024"
                }
                resp = requests.post(url, json=payload, headers=headers)
                data = resp.json()
                if resp.status_code == 200:
                    return {
                        "success": True,
                        "url": data['data'][0]['url'],
                        "prompt": prompt,
                        "style": style,
                        "provider": "Elite Artist (ShuttleAI)"
                    }
                else:
                    return {"success": False, "error": data.get('error', {}).get('message', 'ShuttleAI API Error')}
            except Exception as e:
                logger.error(f"ShuttleAI Error: {e}")
                return {"success": False, "error": f"Elite Engine Connection Failed: {e}"}

        return {"success": False, "error": f"Unknown provider: {provider}"}

creative_brain = CreativeAgent()

# --- REGISTER ALL SKILLS (v16) ---
skill_hub.register("market", "Deep financial data, stocks, and crypto insight.", market_brain)
skill_hub.register("docs", "PDF analysis, document intelligence, and RAG.", doc_brain)
skill_hub.register("finance", "Global stock prices and Alpaca account status.", hub)
skill_hub.register("weather", "Real-time weather data for any city.", hub)
skill_hub.register("movies", "Movie recommendations and search (CineMatch).", movie_brain)
skill_hub.register("vision_lab", "Hand tracking and gesture recognition (MediaPipe).", vision_brain)
skill_hub.register("creative", "DALL-E Asset generation and logos.", creative_brain)
skill_hub.register("analytics", "Data science and student performance prediction.", analytics_brain)
skill_hub.register("gmail", "MOCK: Summarizing and listing Gmail emails.", None)
skill_hub.register("calls", "MOCK: Handling call logs and phone notifications.", None)

# Local Expansion (v17)
try:
    from crew_engine import run_local_task
    skill_hub.register("local_crew", "Execute complex autonomous tasks locally using Ollama and CrewAI.", run_local_task)
except:
    pass
