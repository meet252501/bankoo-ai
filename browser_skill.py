"""
Browser Automation Skill for Bankoo AI
Enables web browsing, scraping, and form filling
"""

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️ Playwright not installed. Run: pip install playwright && playwright install")

import re
from bs4 import BeautifulSoup

class BrowserSkill:
    """Browser automation capabilities"""
    
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None
    
    def browse_url(self, url, extract_text=True):
        """
        Browse a URL and extract content
        
        Args:
            url: URL to visit
            extract_text: If True, extract clean text. If False, return HTML
        
        Returns:
            Extracted content
        """
        if not PLAYWRIGHT_AVAILABLE:
            return "❌ Browser automation not available. Install playwright first."
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, wait_until='domcontentloaded', timeout=30000)
                
                if extract_text:
                    # Extract clean text
                    content = page.content()
                    soup = BeautifulSoup(content, 'html.parser')
                    
                    # Remove script and style elements
                    for script in soup(["script", "style"]):
                        script.decompose()
                    
                    text = soup.get_text()
                    lines = (line.strip() for line in text.splitlines())
                    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = '\n'.join(chunk for chunk in chunks if chunk)
                    
                    browser.close()
                    return text[:5000]  # Limit to 5000 chars
                else:
                    html = page.content()
                    browser.close()
                    return html
                    
        except Exception as e:
            return f"❌ Browser error: {e}"
    
    def extract_links(self, url):
        """Extract all links from a page"""
        if not PLAYWRIGHT_AVAILABLE:
            return []
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=30000)
                
                links = page.eval_on_selector_all('a[href]', 
                    'elements => elements.map(e => ({text: e.innerText, href: e.href}))')
                
                browser.close()
                return links
        except Exception as e:
            return []
    
    def screenshot(self, url, output_path='screenshot.png'):
        """Take a screenshot of a webpage"""
        if not PLAYWRIGHT_AVAILABLE:
            return "❌ Playwright not available"
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=30000)
                page.screenshot(path=output_path, full_page=True)
                browser.close()
                return f"✅ Screenshot saved to {output_path}"
        except Exception as e:
            return f"❌ Screenshot error: {e}"
    
    def fill_form(self, url, form_data):
        """
        Fill a form on a webpage
        
        Args:
            url: URL of the page with form
            form_data: Dict of {selector: value} pairs
        
        Example:
            fill_form('https://example.com/form', {
                '#name': 'John Doe',
                '#email': 'john@example.com'
            })
        """
        if not PLAYWRIGHT_AVAILABLE:
            return "❌ Playwright not available"
        
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=False)  # Visible for debugging
                page = browser.new_page()
                page.goto(url, timeout=30000)
                
                for selector, value in form_data.items():
                    page.fill(selector, value)
                
                # Don't auto-submit - let user confirm
                input("Form filled. Press Enter to close browser...")
                browser.close()
                return "✅ Form filled successfully"
        except Exception as e:
            return f"❌ Form fill error: {e}"
    
    def search_google(self, query):
        """Fast multi-source web search with Wikipedia and Reddit"""
        try:
            import requests
            from bs4 import BeautifulSoup
            import logging
            logger = logging.getLogger(__name__)
            
            logger.info(f"🔍 Multi-source search for: {query}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Method 1: Wikipedia API (excellent for factual queries)
            try:
                wiki_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={query}&limit=5&format=json"
                wiki_resp = requests.get(wiki_url, timeout=5)
                if wiki_resp.status_code == 200:
                    data = wiki_resp.json()
                    titles = data[1] if len(data) > 1 else []
                    descriptions = data[2] if len(data) > 2 else []
                    
                    if titles and len(titles) > 0:
                        result = f"Search results for '{query}':\n\n"
                        for i, (title, desc) in enumerate(zip(titles, descriptions), 1):
                            result += f"{i}. {title}\n"
                            if desc:
                                result += f"   {desc}\n\n"
                        
                        logger.info(f"✅ Found {len(titles)} Wikipedia results")
                        return result
            except Exception as e:
                logger.debug(f"Wikipedia failed: {e}")
            
            # Method 2: Reddit JSON (great for "best X" queries)
            try:
                # Reddit's JSON endpoint doesn't require API key
                reddit_query = query.replace(' ', '+')
                reddit_url = f"https://www.reddit.com/search.json?q={reddit_query}&limit=5&sort=relevance"
                reddit_resp = requests.get(reddit_url, headers={**headers, 'User-Agent': 'BankooAI/1.0'}, timeout=8)
                
                if reddit_resp.status_code == 200:
                    data = reddit_resp.json()
                    posts = data.get('data', {}).get('children', [])
                    
                    if posts and len(posts) > 0:
                        result = f"Search results for '{query}' (from Reddit):\n\n"
                        for i, post_data in enumerate(posts[:5], 1):
                            post = post_data.get('data', {})
                            title = post.get('title', '')
                            selftext = post.get('selftext', '')
                            subreddit = post.get('subreddit', '')
                            
                            if title:
                                result += f"{i}. {title}\n"
                                result += f"   r/{subreddit}\n"
                                if selftext and len(selftext) > 0:
                                    result += f"   {selftext[:150]}...\n\n"
                                else:
                                    result += "\n"
                        
                        logger.info(f"✅ Found {len(posts)} Reddit results")
                        return result
            except Exception as e:
                logger.debug(f"Reddit failed: {e}")
            
            # Method 3: DuckDuckGo Instant Answer API (backup)
            try:
                instant_url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1"
                instant_resp = requests.get(instant_url, timeout=5)
                if instant_resp.status_code == 200:
                    data = instant_resp.json()
                    abstract = data.get('Abstract', '')
                    heading = data.get('Heading', '')
                    
                    if abstract and len(abstract) > 50:
                        result = f"Search results for '{query}':\n\n"
                        result += f"📌 {heading}\n\n" if heading else ""
                        result += f"{abstract}\n"
                        
                        logger.info("✅ Found DuckDuckGo instant answer")
                        return result
            except Exception as e:
                logger.debug(f"DuckDuckGo failed: {e}")
            
            # All methods failed
            logger.warning("All search methods failed, returning None")
            return None
                
        except Exception as e:
            logger.error(f"Search error: {e}")
            return None

# Global instance
browser_skill = BrowserSkill()
