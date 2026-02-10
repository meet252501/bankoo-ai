from playwright.sync_api import sync_playwright

query = "weather in tokyo"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set to False to see what happens
    page = browser.new_page()
    page.goto(f'https://www.google.com/search?q={query}', timeout=30000)
    
    # Wait for results to load
    page.wait_for_timeout(2000)
    
    # Save screenshot for debugging
    page.screenshot(path="google_search_debug.png")
    
    # Try to get page content
    content = page.content()
    print(f"Page content length: {len(content)} chars")
    
    # Try different selectors
    print("\n=== Testing Selectors ===")
    
    # Original selector
    results1 = page.query_selector_all('.g')
    print(f".g elements: {len(results1)}")
    
    # Alternative selectors
    results2 = page.query_selector_all('div[data-sokoban-container]')
    print(f"div[data-sokoban-container]: {len(results2)}")
    
    results3 = page.query_selector_all('.MjjYud')
    print(f".MjjYud: {len(results3)}")
    
    # Print first result if found
    if results3:
        first = results3[0]
        title = first.query_selector('h3')
        snippet = first.query_selector('.VwiC3b')
        print(f"\nFirst result:")
        print(f"  Title: {title.inner_text() if title else 'None'}")
        print(f"  Snippet: {snippet.inner_text() if snippet else 'None'}")
    
    input("Press Enter to close browser...")
    browser.close()
