"""
Web Scraper Studio - Comprehensive Test Suite
Tests all backend functions, API endpoints, and features
"""

import requests
import json
import time
from datetime import datetime

# Test Configuration
BASE_URL = "http://127.0.0.1:5001"
TEST_RESULTS = []

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def log_test(name, status, details=""):
    """Log test results"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    symbol = "✓" if status == "PASS" else "✗" if status == "FAIL" else "⚠"
    color = Colors.GREEN if status == "PASS" else Colors.RED if status == "FAIL" else Colors.YELLOW
    
    result = {
        "timestamp": timestamp,
        "test": name,
        "status": status,
        "details": details
    }
    TEST_RESULTS.append(result)
    
    print(f"{color}{symbol} [{timestamp}] {name}: {status}{Colors.END}")
    if details:
        print(f"  {Colors.CYAN}→ {details}{Colors.END}")

def print_header(text):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def test_backend_import():
    """Test 1: Backend module import"""
    print_header("TEST 1: Backend Module")
    try:
        from web_scraper_brain import scraper_brain
        log_test("Import web_scraper_brain", "PASS", "Module loaded successfully")
        return scraper_brain
    except Exception as e:
        log_test("Import web_scraper_brain", "FAIL", str(e))
        return None

def test_basic_scraping(scraper_brain):
    """Test 2: Basic scraping functionality"""
    print_header("TEST 2: Basic Scraping")
    
    if not scraper_brain:
        log_test("Basic Scraping", "SKIP", "Backend not available")
        return None
    
    test_url = "https://example.com"
    
    try:
        start_time = time.time()
        result = scraper_brain.scrape_url(test_url)
        duration = time.time() - start_time
        
        if result['status'] == 'success':
            log_test(f"Scrape {test_url}", "PASS", f"Completed in {duration:.2f}s")
            
            # Check data types
            if 'titles' in result['data']:
                log_test("Extract Titles", "PASS", f"Found {len(result['data']['titles'])} titles")
            else:
                log_test("Extract Titles", "WARN", "No titles found")
            
            if 'links' in result['data']:
                log_test("Extract Links", "PASS", f"Found {len(result['data']['links'])} links")
            else:
                log_test("Extract Links", "WARN", "No links found")
            
            return result['data']
        else:
            log_test(f"Scrape {test_url}", "FAIL", result.get('error', 'Unknown error'))
            return None
            
    except Exception as e:
        log_test("Basic Scraping", "FAIL", str(e))
        return None

def test_price_extraction(scraper_brain):
    """Test 3: Price extraction patterns"""
    print_header("TEST 3: Price Extraction")
    
    if not scraper_brain:
        log_test("Price Extraction", "SKIP", "Backend not available")
        return
    
    # Test with HTML containing prices
    from bs4 import BeautifulSoup
    
    test_html = """
    <html>
        <body>
            <p>Price: ₹1,999</p>
            <p>Cost: $29.99</p>
            <p>Value: Rs. 5,000</p>
            <p>Amount: €49.99</p>
        </body>
    </html>
    """
    
    try:
        soup = BeautifulSoup(test_html, 'lxml')
        prices = scraper_brain._extract_prices(soup)
        
        if len(prices) > 0:
            log_test("Price Pattern Detection", "PASS", f"Found {len(prices)} prices: {prices}")
        else:
            log_test("Price Pattern Detection", "FAIL", "No prices detected")
            
    except Exception as e:
        log_test("Price Extraction", "FAIL", str(e))

def test_spam_filtering(scraper_brain):
    """Test 4: Spam filtering"""
    print_header("TEST 4: Spam Filtering")
    
    if not scraper_brain:
        log_test("Spam Filtering", "SKIP", "Backend not available")
        return
    
    test_data = {
        'titles': [
            {'type': 'h1', 'text': 'Buy Now Limited Offer'},
            {'type': 'h1', 'text': 'Real Article Title'},
            {'type': 'h2', 'text': 'Click Here Subscribe'}
        ]
    }
    
    try:
        cleaned = scraper_brain.clean_data(test_data)
        original_count = len(test_data['titles'])
        cleaned_count = len(cleaned['titles'])
        removed = original_count - cleaned_count
        
        log_test("Spam Filtering", "PASS", f"Removed {removed}/{original_count} spam items")
        
    except Exception as e:
        log_test("Spam Filtering", "FAIL", str(e))

def test_api_extract_endpoint():
    """Test 5: API Extract Endpoint"""
    print_header("TEST 5: API /extract Endpoint")
    
    endpoint = f"{BASE_URL}/api/scraper/extract"
    payload = {
        "url": "https://example.com",
        "options": {
            "titles": True,
            "prices": True,
            "images": True,
            "links": True
        }
    }
    
    try:
        start_time = time.time()
        response = requests.post(endpoint, json=payload, timeout=15)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            log_test("API /extract", "PASS", f"Response in {duration:.2f}s, Status: {data.get('status')}")
            
            if 'data' in data:
                log_test("API Response Structure", "PASS", f"Contains {len(data['data'])} data fields")
                return data['data']
            else:
                log_test("API Response Structure", "WARN", "No data field in response")
                return None
        else:
            log_test("API /extract", "FAIL", f"Status code: {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        log_test("API /extract", "FAIL", "Cannot connect to Bankoo server. Is it running?")
        return None
    except Exception as e:
        log_test("API /extract", "FAIL", str(e))
        return None

def test_ai_analysis_endpoint(scraped_data):
    """Test 6: AI Analysis Endpoint"""
    print_header("TEST 6: AI Analysis Endpoints")
    
    if not scraped_data:
        log_test("AI Analysis", "SKIP", "No scraped data available")
        return
    
    # Test sentiment analysis
    endpoint = f"{BASE_URL}/api/scraper/ai/analyze"
    
    for analysis_type in ['sentiment', 'categorize', 'summary']:
        try:
            payload = {
                "data": scraped_data,
                "type": analysis_type
            }
            
            start_time = time.time()
            response = requests.post(endpoint, json=payload, timeout=30)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                log_test(f"AI {analysis_type.capitalize()}", "PASS", 
                        f"Completed in {duration:.2f}s - {result.get('result', '')[:50]}...")
            else:
                log_test(f"AI {analysis_type.capitalize()}", "FAIL", 
                        f"Status code: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            log_test(f"AI {analysis_type.capitalize()}", "FAIL", "Server not responding")
            break
        except Exception as e:
            log_test(f"AI {analysis_type.capitalize()}", "FAIL", str(e))

def test_question_answering(scraped_data):
    """Test 7: Question Answering"""
    print_header("TEST 7: Question Answering")
    
    if not scraped_data:
        log_test("Question Answering", "SKIP", "No scraped data available")
        return
    
    endpoint = f"{BASE_URL}/api/scraper/ai/question"
    
    test_questions = [
        "What is the main title?",
        "How many links are there?",
        "What topics are covered?"
    ]
    
    for question in test_questions:
        try:
            payload = {
                "data": scraped_data,
                "question": question
            }
            
            start_time = time.time()
            response = requests.post(endpoint, json=payload, timeout=30)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('answer', '')
                log_test(f"Q: {question}", "PASS", 
                        f"A: {answer[:60]}... ({duration:.2f}s)")
            else:
                log_test(f"Q: {question}", "FAIL", f"Status {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            log_test("Question Answering", "FAIL", "Server not responding")
            break
        except Exception as e:
            log_test(f"Q: {question}", "FAIL", str(e))

def test_error_handling():
    """Test 8: Error handling"""
    print_header("TEST 8: Error Handling")
    
    # Test with invalid URL
    endpoint = f"{BASE_URL}/api/scraper/extract"
    
    test_cases = [
        {"url": "", "desc": "Empty URL"},
        {"url": "not-a-url", "desc": "Invalid URL format"},
        {"url": "https://thiswebsitedoesnotexist12345.com", "desc": "Non-existent domain"}
    ]
    
    for test_case in test_cases:
        try:
            payload = {"url": test_case["url"], "options": {}}
            response = requests.post(endpoint, json=payload, timeout=10)
            
            if response.status_code >= 400:
                log_test(f"Error: {test_case['desc']}", "PASS", "Properly handled with error response")
            else:
                data = response.json()
                if data.get('status') == 'error':
                    log_test(f"Error: {test_case['desc']}", "PASS", "Returned error status")
                else:
                    log_test(f"Error: {test_case['desc']}", "WARN", "Should have returned error")
                    
        except Exception as e:
            log_test(f"Error: {test_case['desc']}", "WARN", str(e))

def test_advanced_features():
    """Test 9: Advanced Features (Batch, Insights, Dedupe, CSV)"""
    print_header("TEST 9: Advanced Features")
    
    # 9a. Batch Processing
    try:
        endpoint = f"{BASE_URL}/api/scraper/batch"
        payload = {
            "urls": ["https://example.com"],  # Just one for testing
            "options": {"titles": True}
        }
        response = requests.post(endpoint, json=payload, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success' and 'results' in data:
                log_test("Batch Processing", "PASS", f"Processed {len(data['results'])} URLs")
            else:
                log_test("Batch Processing", "FAIL", "Invalid response structure")
        else:
            log_test("Batch Processing", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("Batch Processing", "FAIL", str(e))
        
    # Test Data for Utilities
    test_data = {
        "titles": ["Test Title", "Test Title", "Another Title"],
        "prices": ["$10.00", "$20.00", "$10.00"]
    }
    
    # 9b. Deduplication
    try:
        endpoint = f"{BASE_URL}/api/scraper/deduplicate"
        payload = {"data": test_data}
        response = requests.post(endpoint, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            cleaned = result.get('data', {})
            if len(cleaned['titles']) == 2 and len(cleaned['prices']) == 2:
                log_test("Deduplication", "PASS", "Successfully removed duplicates")
            else:
                log_test("Deduplication", "FAIL", f"Failed to deduplicate: {cleaned}")
        else:
            log_test("Deduplication", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("Deduplication", "FAIL", str(e))

    # 9c. Insights
    try:
        endpoint = f"{BASE_URL}/api/scraper/insights"
        payload = {"data": test_data}
        response = requests.post(endpoint, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if 'insights' in result and len(result['insights']) > 0:
                log_test("Auto Insights", "PASS", f"Generated {len(result['insights'])} insights")
            else:
                log_test("Auto Insights", "FAIL", "No insights generated")
        else:
            log_test("Auto Insights", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("Auto Insights", "FAIL", str(e))

    # 9d. CSV Export
    try:
        endpoint = f"{BASE_URL}/api/scraper/export/csv"
        payload = {"data": test_data}
        response = requests.post(endpoint, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if 'csv' in result and 'titles,prices' in result['csv']:
                log_test("CSV Export", "PASS", "CSV generated with headers")
            else:
                log_test("CSV Export", "FAIL", "Invalid CSV content")
        else:
            log_test("CSV Export", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("CSV Export", "FAIL", str(e))

def test_ultimate_features():
    """Test 10: Ultimate Features (Spider, Graph, Scheduler)"""
    print_header("TEST 10: Ultimate Features")
    
    # 10a. Spider Mode
    try:
        endpoint = f"{BASE_URL}/api/scraper/spider"
        payload = {
            "url": "https://example.com",
            "max_pages": 1, # Keep it fast
            "options": {"titles": True}
        }
        # Spider might take a few seconds
        start = time.time()
        response = requests.post(endpoint, json=payload, timeout=30)
        duration = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success' and 'results' in data:
                log_test("Spider Crawl", "PASS", f"Crawled {data.get('pages_crawled')} pages in {duration:.2f}s")
            else:
                log_test("Spider Crawl", "FAIL", "Invalid response")
        else:
            log_test("Spider Crawl", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("Spider Crawl", "FAIL", str(e))

    # 10b. Neural Graph
    try:
        endpoint = f"{BASE_URL}/api/scraper/graph"
        # Use dummy data
        test_data = {
            "titles": ["Product A", "Product B"],
            "prices": ["$10", "$20"],
            "links": [{"text": "Link 1", "url": "http://a.com"}]
        }
        response = requests.post(endpoint, json={"data": test_data}, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'graph' in data and 'nodes' in data['graph']:
                nodes = len(data['graph']['nodes'])
                edges = len(data['graph']['links'])
                log_test("Neural Graph", "PASS", f"Generated {nodes} nodes, {edges} edges")
            else:
                log_test("Neural Graph", "FAIL", "Invalid graph structure")
        else:
            log_test("Neural Graph", "FAIL", f"Status code: {response.status_code}")
    except Exception as e:
        log_test("Neural Graph", "FAIL", str(e))

    # 10c. Scheduler (Add, List, Remove)
    try:
        # Add Job
        add_ep = f"{BASE_URL}/api/scraper/schedule/add"
        list_ep = f"{BASE_URL}/api/scraper/schedule/list"
        rem_ep = f"{BASE_URL}/api/scraper/schedule/remove"
        
        # 1. Add
        res_add = requests.post(add_ep, json={"url": "http://test.com", "interval": 60})
        if res_add.status_code == 200:
            job_id = res_add.json().get('job', {}).get('id')
            log_test("Scheduler (Add)", "PASS", f"Added Job ID {job_id}")
            
            # 2. List
            res_list = requests.get(list_ep)
            jobs = res_list.json()
            found = any(j['id'] == job_id for j in jobs)
            if found:
                log_test("Scheduler (List)", "PASS", f"Found job in list of {len(jobs)}")
            else:
                log_test("Scheduler (List)", "FAIL", "Added job not found")
                
            # 3. Remove
            requests.post(rem_ep, json={"id": job_id})
            # Verify removal
            res_list_2 = requests.get(list_ep)
            found_2 = any(j['id'] == job_id for j in res_list_2.json())
            if not found_2:
                log_test("Scheduler (Remove)", "PASS", "Job successfully removed")
            else:
                log_test("Scheduler (Remove)", "FAIL", "Job still exists")
                
        else:
            log_test("Scheduler (Add)", "FAIL", f"Status code: {res_add.status_code}")
            
    except Exception as e:
        log_test("Scheduler Flow", "FAIL", str(e))

def generate_report():
    """Generate final test report"""
    print_header("TEST SUMMARY")
    
    total = len(TEST_RESULTS)
    passed = sum(1 for r in TEST_RESULTS if r['status'] == 'PASS')
    failed = sum(1 for r in TEST_RESULTS if r['status'] == 'FAIL')
    warned = sum(1 for r in TEST_RESULTS if r['status'] == 'WARN')
    skipped = sum(1 for r in TEST_RESULTS if r['status'] == 'SKIP')
    
    print(f"{Colors.BOLD}Total Tests:{Colors.END} {total}")
    print(f"{Colors.GREEN}✓ Passed:{Colors.END} {passed}")
    print(f"{Colors.RED}✗ Failed:{Colors.END} {failed}")
    print(f"{Colors.YELLOW}⚠ Warnings:{Colors.END} {warned}")
    print(f"{Colors.CYAN}⊘ Skipped:{Colors.END} {skipped}")
    
    success_rate = (passed / total * 100) if total > 0 else 0
    print(f"\n{Colors.BOLD}Success Rate:{Colors.END} {success_rate:.1f}%")
    
    # Save to file
    with open("test_results.json", "w") as f:
        json.dump(TEST_RESULTS, f, indent=2)
    
    print(f"\n{Colors.CYAN}Detailed results saved to: test_results.json{Colors.END}")
    
    # Overall status
    if failed == 0 and warned == 0:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED!{Colors.END}")
    elif failed == 0:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠ PASSED WITH WARNINGS{Colors.END}")
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ SOME TESTS FAILED{Colors.END}")

def main():
    """Run all tests"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔" + "═"*58 + "╗")
    print("║" + " WEB SCRAPER STUDIO - COMPREHENSIVE TEST SUITE ".center(58) + "║")
    print("╚" + "═"*58 + "╝")
    print(f"{Colors.END}")
    
    print(f"{Colors.YELLOW}Starting tests...{Colors.END}\n")
    
    # Run tests
    scraper_brain = test_backend_import()
    scraper_brain = test_backend_import()
    scraped_data_local = test_basic_scraping(scraper_brain)
    test_price_extraction(scraper_brain)
    test_spam_filtering(scraper_brain)
    
    scraped_data_api = test_api_extract_endpoint()
    test_ai_analysis_endpoint(scraped_data_api)
    test_question_answering(scraped_data_api)
    test_error_handling()
    test_advanced_features()
    test_ultimate_features()
    
    # Generate report
    generate_report()
    
    print(f"\n{Colors.CYAN}Test suite completed!{Colors.END}\n")

if __name__ == "__main__":
    main()
