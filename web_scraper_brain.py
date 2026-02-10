"""
Web Scraper Studio - Backend Brain
Intelligent web scraping with AI-powered features
"""

from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import urljoin, urlparse
import time

class WebScraperBrain:
    """Main scraping engine with AI capabilities"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_url(self, url, options=None):
        """
        Scrape a URL and extract data based on options
        
        Args:
            url: Website URL to scrape
            options: dict with extraction preferences
        
        Returns:
            dict with scraped data
        """
        if options is None:
            options = {
                'titles': True,
                'prices': True,
                'images': True,
                'links': True,
                'tables': False
            }
        
        # Try fetching with retries (Robust mode)
        tries = 2
        for i in range(tries):
            try:
                print(f"🕷️ [SCRAPER] Fetching ({i+1}/{tries}): {url}")
                response = requests.get(url, headers=self.headers, timeout=25)
                response.raise_for_status()
                break # Success
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                if i == tries - 1: raise e # Last try failed
                print(f"   ⚠️ Connection slow. Retrying in 2s...")
                time.sleep(2)
        
        try:
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extract data
            data = {
                'url': url,
                'status': 'success',
                'data': {}
            }
            
            if options.get('titles'):
                data['data']['titles'] = self._extract_titles(soup)
            
            if options.get('prices'):
                data['data']['prices'] = self._extract_prices(soup)
            
            if options.get('images'):
                data['data']['images'] = self._extract_images(soup, url)
            
            if options.get('links'):
                data['data']['links'] = self._extract_links(soup, url)
            
            if options.get('tables'):
                data['data']['tables'] = self._extract_tables(soup)
            
            # Get full text for AI processing
            data['data']['full_text'] = soup.get_text(separator=' ', strip=True)[:5000]  # Limit to 5000 chars
            
            print(f"✅ [SCRAPER] Extracted {sum(len(v) if isinstance(v, list) else 1 for v in data['data'].values())} items")
            return data
            
        except requests.exceptions.RequestException as e:
            print(f"❌ [SCRAPER] Error: {e}")
            return {
                'url': url,
                'status': 'error',
                'error': str(e)
            }
    
    def _extract_titles(self, soup):
        """Extract all titles and headings"""
        titles = []
        
        # Meta title
        title_tag = soup.find('title')
        if title_tag:
            titles.append({'type': 'page_title', 'text': title_tag.get_text(strip=True)})
        
        # H1, H2, H3 headings
        for tag in ['h1', 'h2', 'h3']:
            for heading in soup.find_all(tag):
                text = heading.get_text(strip=True)
                if text:
                    titles.append({'type': tag, 'text': text})
        
        return titles[:20]  # Limit to 20
    
    def _extract_prices(self, soup):
        """Extract prices using regex patterns"""
        prices = []
        text = soup.get_text()
        
        # Price patterns (₹, $, €, etc.)
        patterns = [
            r'₹\s*[\d,]+(?:\.\d{2})?',  # Indian Rupee
            r'\$\s*[\d,]+(?:\.\d{2})?',  # Dollar
            r'€\s*[\d,]+(?:\.\d{2})?',  # Euro
            r'Rs\.?\s*[\d,]+(?:\.\d{2})?',  # Rs
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                prices.append(match.strip())
        
        # Remove duplicates, keep unique
        return list(set(prices))[:50]
    
    def _extract_images(self, soup, base_url):
        """Extract image URLs"""
        images = []
        
        for img in soup.find_all('img', src=True):
            src = img.get('src')
            if src:
                # Convert relative URLs to absolute
                abs_url = urljoin(base_url, src)
                alt = img.get('alt', '')
                images.append({
                    'url': abs_url,
                    'alt': alt
                })
        
        return images[:30]  # Limit to 30
    
    def _extract_links(self, soup, base_url):
        """Extract all links"""
        links = []
        
        for a in soup.find_all('a', href=True):
            href = a.get('href')
            text = a.get_text(strip=True)
            
            if href:
                abs_url = urljoin(base_url, href)
                links.append({
                    'url': abs_url,
                    'text': text
                })
        
        return links[:50]  # Limit to 50
    
    def _extract_tables(self, soup):
        """Extract data from HTML tables"""
        tables = []
        
        for table in soup.find_all('table'):
            table_data = []
            for row in table.find_all('tr'):
                row_data = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]
                if row_data:
                    table_data.append(row_data)
            
            if table_data:
                tables.append(table_data)
        
        return tables[:5]  # Limit to 5 tables
    
    def clean_data(self, data):
        """Remove spam and clean extracted data"""
        # Simple spam keywords
        spam_keywords = [
            'advertisement', 'sponsored', 'buy now', 'limited offer',
            'click here', 'subscribe', 'sign up'
        ]
        
        cleaned = {}
        
        for key, items in data.items():
            if isinstance(items, list):
                cleaned[key] = [
                    item for item in items
                    if not self._is_spam(str(item), spam_keywords)
                ]
            else:
                cleaned[key] = items
        
        return cleaned
    
    def _is_spam(self, text, spam_keywords):
        """Check if text contains spam"""
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in spam_keywords)
    
    # === ADVANCED FEATURES ===
    
    def scrape_batch(self, urls, options=None):
        """Scrape multiple URLs in batch"""
        results = []
        for idx, url in enumerate(urls, 1):
            print(f"📊 [BATCH] Processing {idx}/{len(urls)}: {url}")
            result = self.scrape_url(url, options)
            results.append(result)
        
        return {
            'status': 'success',
            'total': len(urls),
            'results': results
        }
    
    def deduplicate_data(self, data):
        """Remove duplicate entries from scraped data"""
        if not isinstance(data, dict):
            return data
        
        deduplicated = {}
        
        for key, items in data.items():
            if isinstance(items, list):
                # Remove duplicates while preserving order
                seen = set()
                unique_items = []
                
                for item in items:
                    # Convert to string for comparison
                    item_str = str(item)
                    if item_str not in seen:
                        seen.add(item_str)
                        unique_items.append(item)
                
                deduplicated[key] = unique_items
            else:
                deduplicated[key] = items
        
        return deduplicated
    
    def export_to_csv(self, data):
        """Convert scraped data to CSV format"""
        import csv
        from io import StringIO
        
        output = StringIO()
        
        # Find the longest list to determine row count
        max_rows = 0
        for key, value in data.items():
            if isinstance(value, list):
                max_rows = max(max_rows, len(value))
        
        # Create CSV
        if max_rows > 0:
            fieldnames = [key for key in data.keys() if isinstance(data[key], list)]
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            
            for i in range(max_rows):
                row = {}
                for key in fieldnames:
                    if i < len(data[key]):
                        item = data[key][i]
                        # Convert dict/object to string
                        if isinstance(item, dict):
                            row[key] = ', '.join(f"{k}: {v}" for k, v in item.items())
                        else:
                            row[key] = str(item)
                    else:
                        row[key] = ''
                writer.writerow(row)
        
        return output.getvalue()
    
    def generate_insights(self, data):
        """Generate automated insights from scraped data"""
        insights = []
        
        # Count statistics
        if 'titles' in data and isinstance(data['titles'], list):
            insights.append(f"📰 Found {len(data['titles'])} titles/headings")
        
        if 'prices' in data and isinstance(data['prices'], list):
            price_count = len(data['prices'])
            insights.append(f"💰 Detected {price_count} prices")
            
            # Price analysis
            if price_count > 0:
                # Try to extract numeric values for analysis
                numeric_prices = []
                for price in data['prices']:
                    # Extract numbers
                    numbers = re.findall(r'[\d,]+(?:\.\d{2})?', str(price))
                    if numbers:
                        try:
                            # Remove commas and convert
                            val = float(numbers[0].replace(',', ''))
                            numeric_prices.append(val)
                        except:
                            pass
                
                if numeric_prices:
                    avg_price = sum(numeric_prices) / len(numeric_prices)
                    min_price = min(numeric_prices)
                    max_price = max(numeric_prices)
                    insights.append(f"📊 Price range: {min_price:.2f} - {max_price:.2f} (avg: {avg_price:.2f})")
        
        if 'images' in data and isinstance(data['images'], list):
            insights.append(f"🖼️ Found {len(data['images'])} images")
        
        if 'links' in data and isinstance(data['links'], list):
            link_count = len(data['links'])
            insights.append(f"🔗 Extracted {link_count} links")
            
            # Check for broken/external links
            if link_count > 0:
                external_links = sum(1 for link in data['links'] if isinstance(link, dict) and 'url' in link and not link['url'].startswith('#'))
                insights.append(f"🌐 {external_links} external links")
        
        if 'tables' in data and isinstance(data['tables'], list):
            insights.append(f"📋 Found {len(data['tables'])} tables")
        
        return insights
    
    # === SPIDER MODE (CRAWLER) ===
    
    def scrape_spider(self, start_url, max_pages=5, same_domain=True, options=None):
        """
        Recursively scrape pages starting from a URL
        
        Args:
            start_url: URL to start crawling
            max_pages: Maximum number of pages to crawl
            same_domain: Restrict to same domain
            options: Extraction options
        """
        results = []
        queue = [start_url]
        visited = set()
        base_domain = urlparse(start_url).netloc
        
        print(f"🕷️ [SPIDER] Starting crawl from: {start_url} (Max: {max_pages})")
        
        while queue and len(visited) < max_pages:
            current_url = queue.pop(0)
            
            if current_url in visited:
                continue
                
            # Domain check
            if same_domain and urlparse(current_url).netloc != base_domain:
                continue
                
            # Scrape content
            print(f"🕸️ [SPIDER] Crawling ({len(visited)+1}/{max_pages}): {current_url}")
            data = self.scrape_url(current_url, options)
            
            if data.get('status') == 'success':
                results.append(data)
                visited.add(current_url)
                
                # Find next pages
                # 1. Look for 'next' info in links
                # 2. Add to queue
                if 'links' in data['data']:
                    new_links = self._find_next_links(data['data']['links'], visited, base_domain if same_domain else None)
                    for link in new_links:
                        if link not in visited and link not in queue:
                            queue.append(link)
                            
            time.sleep(1)  # Polite delay
            
        return {
            'status': 'success',
            'pages_crawled': len(visited),
            'results': results
        }
    
    def _find_next_links(self, links, visited, restrict_domain=None):
        """Heuristic to find 'next' or valid content links"""
        candidates = []
        
        keywords = ['next', 'more', 'page', 'Older posts']
        
        for link in links:
            if not isinstance(link, dict) or 'url' not in link:
                continue
                
            url = link['url']
            text = link.get('text', '').lower()
            
            # Skip visited
            if url in visited:
                continue
                
            # Domain check
            if restrict_domain and urlparse(url).netloc != restrict_domain:
                continue
            
            # Heuristic: If text contains 'next' or it looks like a pagination link
            is_candidate = False
            
            # 1. Keyword match
            if any(k in text for k in keywords):
                is_candidate = True
            
            # 2. Numbered pagination (e.g., /page/2)
            if re.search(r'/page/\d+', url):
                is_candidate = True
                
            # 3. Query param pagination (e.g., ?p=2)
            if re.search(r'[?&](p|page|start)=\d+', url):
                is_candidate = True
                
            if is_candidate:
                candidates.append(url)
                
        # If no obvious pagination found, maybe return all valid internal links?
        # For safety/speed, let's only return high-confidence pagination candidates for now
        # OR return first 5 unvisited links to simulate "crawling"
        
        if not candidates:
            # Fallback: BFS behavior - add up to 3 unvisited internal links
            count = 0
            for link in links:
                if isinstance(link, dict) and 'url' in link:
                    url = link['url']
                    if url not in visited and (not restrict_domain or urlparse(url).netloc == restrict_domain):
                        candidates.append(url)
                        count += 1
                        if count >= 3:
                            break
                            
        return candidates

    def universal_extract(self, url, query, ai_client, model_id):
        """
        AI-Powered Universal Extraction.
        Fetches HTML -> Cleans it -> Asks LLM to extract JSON.
        """
        try:
            # 1. Fetch
            print(f"✨ [AI SCRAPER] Fetching for universal extract: {url}")
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            # 2. Parse & Clean aggressively
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Remove junk
            for tag in soup(['script', 'style', 'nav', 'footer', 'iframe', 'noscript', 'svg']):
                tag.decompose()
                
            # Get structured text/html subset
            # We treat 'main', 'article', or 'body' as core
            core = soup.find('main') or soup.find('article') or soup.body
            clean_html = str(core)[:15000] # Limit tokens (approx 4k tokens)
            
            # 3. Prompt AI
            system_prompt = "You are a specialized Web Scraper Agent. Your job is to extract data from HTML into clean JSON. If the user asks for a list, ensure you extract ALL matching items, not just one."
            user_prompt = f"""
            Task: Extract data matching this description: "{query}"
            
            Instructions:
            - Return ONLY valid JSON.
            - If extracting a list (e.g. products, prices), return a JSON Array or an Object with a list property.
            - Do not include markdown formatting (```json).
            - If data is missing, use null or empty string.

            HTML Input:
            {clean_html}
            """
            
            print(f"🧠 [AI SCRAPER] Analysis started using {model_id}...")
            # Use the passed client (from assistant)
            response = ai_client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            result_json = response.choices[0].message.content
            return {"status": "success", "data": result_json}
        
        except Exception as e:
            print(f"❌ [AI SCRAPER] Error: {e}")
            return {"status": "error", "error": str(e)}

    def generate_graph(self, data):
        """Generate network graph nodes and edges from data"""
        nodes = []
        edges = []
        
        # Helper
        def add_node(id, label, group):
            # Check dupes
            if not any(n['id'] == id for n in nodes):
                nodes.append({
                    'id': id, 
                    'label': str(label)[:30] + ('...' if len(str(label)) > 30 else ''), 
                    'group': group,
                    'title': str(label) # Full text for tooltip/click
                })
        
        # Root Node (URL)
        url = data.get('url', 'Current Page')
        add_node('root', url, 'url')
        
        # Titles
        for i, t in enumerate(data.get('titles', [])):
            txt = t.get('text', '') if isinstance(t, dict) else str(t)
            nid = f't_{i}'
            add_node(nid, txt, 'title')
            edges.append({'from': 'root', 'to': nid})
            
        # Prices
        for i, p in enumerate(data.get('prices', [])):
            nid = f'p_{i}'
            add_node(nid, f"💲{p}", 'price')
            edges.append({'from': 'root', 'to': nid})
            
            # Try to link Price to Title (heuristic: same index)
            if i < len(data.get('titles', [])):
                 edges.append({'from': f't_{i}', 'to': nid, 'dashes': True})

        # Links (limit to 10 to avoid clutter)
        for i, l in enumerate(data.get('links', [])[:10]):
             if isinstance(l, dict) and 'url' in l:
                 nid = f'l_{i}'
                 add_node(nid, l['url'], 'link')
                 edges.append({'from': 'root', 'to': nid})
        
        # Magic Data (AI Extracted)
        if 'magic' in data:
            # If magic is list
            mdata = data['magic']
            if isinstance(mdata, list):
                for i, item in enumerate(mdata):
                    nid = f'm_{i}'
                    label = str(item)[:20]
                    if isinstance(item, dict) and 'product_name' in item:
                        label = item['product_name']
                    add_node(nid, label, 'magic')
                    edges.append({'from': 'root', 'to': nid})
                    
        return {'nodes': nodes, 'edges': edges}

# Global instance
scraper_brain = WebScraperBrain()
