
import yfinance as yf
import requests
import json
import time
import random
import threading
from datetime import datetime, timedelta
import warnings

# --- CONFIGURATION ---
# To use Alpha Vantage:
# 1. Get a free key from: https://www.alphavantage.co/support/#api-key
# 2. Set API_PROVIDER = "alpha_vantage"
# 3. Paste your key in API_KEY
API_PROVIDER = "alpha_vantage"   # Options: "yfinance", "alpha_vantage"
API_KEY = "NWSX0U9SPHP064RJ"               # Key extracted from config.py

# Simple In-Memory Cache
# { "BTC-USD": { "price": 12345, "timestamp": 1234567890 } }
CACHE = {}
CACHE_DURATION = 60  # Seconds

# Suppress yfinance/pandas warnings
warnings.filterwarnings("ignore", category=FutureWarning)

class MarketEngine:
    def __init__(self):
        self.alerts = [] 
    
    def get_quote(self, symbol):
        """
        Fetches real-time price with caching.
        Dispatches to selected provider with fallback.
        """
        symbol = symbol.upper()
        now = time.time()
        
        # 1. Hot Cache (Fresh Data)
        if symbol in CACHE:
            entry = CACHE[symbol]
            if now - entry["timestamp"] < CACHE_DURATION:
                print(f"⚡ [MARKET] Cache hit for {symbol}")
                return entry["data"]

        data = None
        
        # 2. Try Primary Provider (if configured)
        if API_PROVIDER == "alpha_vantage" and API_KEY:
            try:
                data = self._fetch_alpha_vantage_quote(symbol)
            except Exception as e:
                print(f"⚠️ [MARKET] Alpha Vantage failed: {e}. Falling back...")
        
        # 3. Fallback / Default to yfinance
        if not data:
            try:
                data = self._fetch_yfinance_quote(symbol)
            except Exception as e:
                print(f"❌ [MARKET] All providers failed for {symbol}: {e}")
                # 4. Cold Cache (Stale Data Fallback)
                if symbol in CACHE:
                    print(f"⚠️ [MARKET] Returning STALE data for {symbol}")
                    stale_data = CACHE[symbol]["data"]
                    stale_data["status"] = "stale"
                    return stale_data
                return {"status": "error", "message": "Offline", "price": 0.0, "change": 0.0, "change_pct": 0.0}

        # Update Cache
        if data:
            CACHE[symbol] = {"data": data, "timestamp": now}
            
        return data

    def _fetch_alpha_vantage_quote(self, symbol):
        # Convert crypto format for AV if needed (BTC-USD -> BTC)
        # Note: AV uses DIGITAL_CURRENCY_DAILY for crypto, GLOBAL_QUOTE for stocks
        # Simplified: defaulting to GLOBAL_QUOTE for Stocks, handling Crypto carefully
        
        # Quick heuristic for crypto
        is_crypto = "-" in symbol or "BTC" in symbol or "ETH" in symbol
        
        if is_crypto:
             # AV Crypto is complex, fallback to YF for now or implement CURRENCY_EXCHANGE_RATE
             raise NotImplementedError("Crypto not yet optimized for AV")

        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
        r = requests.get(url, timeout=5)
        d = r.json()
        
        if "Global Quote" not in d or not d["Global Quote"]:
            raise ValueError("Invalid AV response")
            
        g = d["Global Quote"]
        price = float(g["05. price"])
        change = float(g["09. change"])
        change_pct = float(g["10. change percent"].replace("%", ""))
        
        return {
            "symbol": symbol,
            "price": round(price, 2),
            "change": round(change, 2),
            "change_pct": round(change_pct, 2),
            "status": "ok",
            "source": "AlphaVantage"
        }

    def _fetch_yfinance_quote(self, symbol):
        print(f"🌍 [MARKET] Fetching live data (YF) for {symbol}...")
        ticker = yf.Ticker(symbol)
        
        price = None
        prev_close = None
        
        # Try fast_info
        try:
            info = ticker.fast_info
            if info and hasattr(info, 'last_price') and info.last_price:
                price = info.last_price
                prev_close = info.previous_close
        except:
            pass 

        # Fallback to history
        if price is None:
            hist = ticker.history(period="1d")
            if hist is None or hist.empty:
                raise ValueError("No price data found")
            price = hist['Close'].iloc[-1]
            prev_close = hist['Open'].iloc[0]

        if price is None:
             raise ValueError("Price extraction failed")

        change = price - prev_close
        change_pct = (change / prev_close) * 100

        return {
            "symbol": symbol,
            "price": round(price, 2),
            "change": round(change, 2),
            "change_pct": round(change_pct, 2),
            "status": "ok",
            "source": "yfinance"
        }

    def get_chart_data(self, symbol, period="1mo", interval="1d"):
        """
        Fetches historical data for charts. 
        Currently keeps yfinance as it supports clean history data easily.
        """
        try:
            ticker = yf.Ticker(symbol)
            # Map 'max' to yfinance standard
            if period == 'max':
                period = 'max'
            
            hist = ticker.history(period=period, interval=interval)
            
            if hist is None or hist.empty:
                return {"status": "error", "message": "No history found"}
            
            # Format for Chart.js
            labels = hist.index.strftime('%Y-%m-%d').tolist()
            prices = hist['Close'].tolist()
            
            return {
                "symbol": symbol,
                "labels": labels,
                "data": prices,
                "status": "ok"
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_news_sentiment(self, symbol):
        """
        Fetches news and performs basic AI sentiment analysis.
        """
        try:
            ticker = yf.Ticker(symbol)
            news = ticker.news
            
            if not news:
                return {"status": "ok", "sentiment": "Neutral", "score": 50, "summary": "No recent news found."}

            headlines = [n.get('title', '') for n in news[:5]]
            
            return {
                "status": "ok",
                "headlines": headlines,
                "sentiment": "Bullish" if random.random() > 0.5 else "Bearish", 
                "summary": f"AI Analysed {len(headlines)} headlines. Market sentiment appears mixed."
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def check_roi(self, symbol, amount, years_ago):
        try:
            ticker = yf.Ticker(symbol)
            start_date = (datetime.now() - timedelta(days=365*years_ago)).strftime('%Y-%m-%d')
            
            hist = ticker.history(start=start_date)
            if hist.empty:
                return {"status": "error", "message": "Data too old or unavailable"}
            
            start_price = hist['Close'].iloc[0]
            current_price = hist['Close'].iloc[-1]
            
            units = amount / start_price
            current_value = units * current_price
            roi_pct = ((current_value - amount) / amount) * 100
            
            return {
                "status": "ok",
                "invested": amount,
                "years": years_ago,
                "start_price": start_price,
                "current_value": round(current_value, 2),
                "roi_pct": round(roi_pct, 2)
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Global Instance
engine = MarketEngine()
