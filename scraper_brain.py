import requests
import json
import time
import os
import threading
import uuid
import logging
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Configure Logger for Scraper
logger = logging.getLogger("scraper-brain")

class ScraperBrain:
    def __init__(self):
        self.history = []
        self.scheduler_lock = threading.Lock()
        self.scheduled_jobs = {}
        self.active_spider = False
        
        # Start Scheduler Thread
        threading.Thread(target=self._scheduler_loop, daemon=True).start()

    # --- CORE SCRAPER LOGIC ---
    def extract(self, url, options=None):
        """Extracts data from a single URL based on options."""
        if not options:
            options = {"titles": True}

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            data = {}
            
            # Titles (h1-h3)
            if options.get('titles'):
                data['titles'] = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])]

            # Prices (approximation)
            if options.get('prices'):
                # Heuristic: Look for elements with currency symbols
                prices = []
                for el in soup.find_all(string=True):
                    text = el.strip()
                    if text and any(c in text for c in ['$', '£', '€', '₹']):
                        if len(text) < 20: # Sanity check for price length
                             prices.append(text)
                data['prices'] = list(set(prices)) # Deduplicate

            # Images
            if options.get('images'):
                images = []
                for img in soup.find_all('img'):
                    src = img.get('src')
                    if src:
                        images.append(urljoin(url, src))
                data['images'] = images[:50] # Limit to 50

            # Links
            if options.get('links'):
                links = []
                for a in soup.find_all('a', href=True):
                    links.append({"text": a.get_text(strip=True), "url": urljoin(url, a['href'])})
                data['links'] = links[:50]

            # Tables
            if options.get('tables'):
                 tables = []
                 for t in soup.find_all('table'):
                     tables.append(str(t))
                 data['tables'] = tables

            return {"data": data}

        except Exception as e:
            return {"error": str(e)}

    def extract_js(self, url, options=None):
        """🔥 HEADLESS BROWSER - Extracts data from JavaScript-heavy sites using Playwright."""
        if not options:
            options = {"titles": True}

        try:
            from playwright.sync_api import sync_playwright
            
            with sync_playwright() as p:
                # Launch headless browser
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                
                # Navigate and wait for page load
                page.goto(url, wait_until='networkidle', timeout=30000)
                
                # Wait a bit more for dynamic content
                page.wait_for_timeout(2000)
                
                # Get rendered HTML
                html = page.content()
                browser.close()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            data = {}
            
            # Same extraction logic as extract()
            if options.get('titles'):
                data['titles'] = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])]
            
            if options.get('prices'):
                prices = []
                for el in soup.find_all(string=True):
                    text = el.strip()
                    if text and any(c in text for c in ['$', '£', '€', '₹']):
                        if len(text) < 20:
                             prices.append(text)
                data['prices'] = list(set(prices))
            
            if options.get('images'):
                images = []
                for img in soup.find_all('img'):
                    src = img.get('src')
                    if src:
                        images.append(urljoin(url, src))
                data['images'] = images[:50]
            
            if options.get('links'):
                links = []
                for a in soup.find_all('a', href=True):
                    links.append({"text": a.get_text(strip=True), "url": urljoin(url, a['href'])})
                data['links'] = links[:50]
            
            if options.get('tables'):
                 tables = []
                 for t in soup.find_all('table'):
                     tables.append(str(t))
                 data['tables'] = tables
            
            logger.info(f"✅ Headless scrape complete: {url}")
            return {"data": data, "method": "headless_browser"}

        except ImportError:
            logger.warning("⚠️ Playwright not installed. Install with: pip install playwright && playwright install chromium")
            return {"error": "Playwright not installed. Falling back to basic scraper."}
        except Exception as e:
            logger.error(f"❌ Headless scrape failed: {e}")
            return {"error": str(e)}

    # --- SPIDER LOGIC ---
    def spider(self, start_url, max_pages=5, options=None):
        """Crawls a website starting from start_url."""
        visited = set()
        queue = [start_url]
        results = []
        
        while queue and len(visited) < max_pages:
            url = queue.pop(0)
            if url in visited: continue
            
            logger.info(f"🕷️ Spider Visiting: {url}")
            res = self.extract(url, options)
            if 'error' not in res:
                results.append({"url": url, "data": res['data']})
                visited.add(url)
                
                # Add new links to queue (same domain only)
                domain = urlparse(start_url).netloc
                if 'links' in res['data']:
                    for l in res['data']['links']:
                        l_url = l['url']
                        if urlparse(l_url).netloc == domain and l_url not in visited:
                            queue.append(l_url)
            else:
                 logger.error(f"Failed to crawl {url}: {res['error']}")
            
            time.sleep(0.5) # Politeness delay

        return {"pages_crawled": len(visited), "results": results}

    # --- AI MAGIC ---
    def ai_universal(self, url, query):
        """Uses Configured AI to extract structured data from a page."""
        try:
            # 1. Fetch Page Content (Text)
            headers = {'User-Agent': 'Mozilla/5.0'}
            resp = requests.get(url, headers=headers, timeout=15)
            # Limit content size for LLM context
            content = BeautifulSoup(resp.text, 'html.parser').get_text()[:8000] 
            
            # 2. Ask AI
            import config
            from assistant import DesktopAssistant
            assistant = DesktopAssistant() # Lazy init to use client
            
            # Use JSON mode if possible or just prompting
            prompt = f"""
            You are a Web Extraction Engine.
            URL: {url}
            QUERY: {query}
            
            Here is the truncated text content of the page:
            ---
            {content}
            ---
            
            INSTRUCTIONS:
            1. Extract the requested data STRICTLY as valid JSON.
            2. Do not include markdown code blocks (```json). Just the raw JSON string.
            3. If data is not found, return empty JSON {{}}.
            """
            
            # Using the fast model or reasoning model depending on complexity
            # For extraction, a smart model is better.
            import openai # Or whatever client wrapper is used
            
            # We'll use the assistant's client directly if available
            assistant._init_ai()
             
            response = assistant.client.chat.completions.create(
                model=config.PRIMARY_MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result = response.choices[0].message.content
            # Cleanup markdown if present
            result = result.replace('```json', '').replace('```', '').strip()
            
            return {"status": "success", "data": result}
            
        except Exception as e:
            return {"status": "error", "error": str(e)}

    # --- BATCH PROCESSING ---
    def batch(self, urls, options):
        results = []
        for url in urls:
            res = self.extract(url, options)
            results.append({"url": url, "data": res.get('data', {})})
        return {"results": results}

    # --- GRAPH GENERATION ---
    def generate_graph(self, data):
        """Converts extracted data into a VISjs compatible node-edge structure."""
        nodes = []
        edges = []
        node_ids = set()
        
        # Central Node (Source)
        root_id = "Source"
        nodes.append({"id": root_id, "label": "Scrape Root", "group": "url", "value": 20})
        node_ids.add(root_id)

        # Helper to add node safely
        def add_node(nid, label, group, val=10):
            if nid not in node_ids:
                nodes.append({"id": nid, "label": label[:20] + "..." if len(label)>20 else label, "title": label, "group": group, "value": val})
                node_ids.add(nid)
            return nid

        if 'titles' in data:
            for i, t in enumerate(data['titles']):
                nid = f"t_{i}"
                add_node(nid, t, "title")
                edges.append({"from": root_id, "to": nid})

        if 'prices' in data:
             for i, p in enumerate(data['prices']):
                nid = f"p_{i}"
                add_node(nid, p, "price")
                # Try to link price to nearest title (heuristic)
                edges.append({"from": root_id, "to": nid})

        if 'links' in data:
             for i, l in enumerate(data['links']):
                nid = f"l_{i}"
                add_node(nid, l.get('url', '#'), "link", 5)
                edges.append({"from": root_id, "to": nid})

        return {"nodes": nodes, "edges": edges}

    # --- SCHEDULER (Watchdog) ---
    def add_schedule(self, url, interval):
        job_id = str(uuid.uuid4())[:8]
        with self.scheduler_lock:
            self.scheduled_jobs[job_id] = {
                "id": job_id,
                "url": url,
                "interval": interval,
                "last_run": 0,
                "runs": 0
            }
        return {"id": job_id, "status": "active"}

    def remove_schedule(self, job_id):
        with self.scheduler_lock:
            if job_id in self.scheduled_jobs:
                del self.scheduled_jobs[job_id]
        return {"status": "removed"}

    def list_schedules(self):
         with self.scheduler_lock:
             return list(self.scheduled_jobs.values())

    def _scheduler_loop(self):
        while True:
            time.sleep(1)
            now = time.time()
            to_run = []
            
            with self.scheduler_lock:
                for jid, job in self.scheduled_jobs.items():
                    if now - job['last_run'] > job['interval']:
                        to_run.append(jid)
            
            for jid in to_run:
                # Execute Job (Silent Scrape)
                with self.scheduler_lock:
                    job = self.scheduled_jobs[jid]
                    job['last_run'] = now
                    job['runs'] += 1
                
                logger.info(f"⏰ Scheduler Running: {job['url']}")
                # In a real app, we'd save this or notify user.
                # For now, we just print/log.
                # self.extract(job['url']) 

    # --- UTILS ---
    def deduplicate(self, data):
        new_data = {}
        for k, v in data.items():
            if isinstance(v, list):
                # Handle list of dicts (links) vs list of strings
                if v and isinstance(v[0], dict):
                    # Dedup by JSON string representation
                    seen = set()
                    unique = []
                    for item in v:
                        s = json.dumps(item, sort_keys=True)
                        if s not in seen:
                            seen.add(s)
                            unique.append(item)
                    new_data[k] = unique
                else:
                    new_data[k] = list(set(v))
            else:
                new_data[k] = v
        return {"data": new_data}

    def export_csv(self, data):
         # Flatten for CSV
         # We need to decide a dominant axis (e.g. titles). 
         # This is tricky for unstructured data so we just make separate columns.
         df_data = {}
         max_len = 0
         
         for k, v in data.items():
             if isinstance(v, list):
                 if v and isinstance(v[0], dict):
                     # For links, maybe just extract URLs
                      v = [i.get('url') for i in v]
                 df_data[k] = v
                 max_len = max(max_len, len(v))
         
         # Pad lists
         for k in df_data:
             df_data[k] += [''] * (max_len - len(df_data[k]))
             
         df = pd.DataFrame(df_data)
         return df.to_csv(index=False)
