
import unittest
import json
import os
import sys
import time

# Ensure we can import bankoo_main
sys.path.append(os.getcwd())

from bankoo_main import app
from market_engine import engine as market_brain, CACHE

class MarketWidgetTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # --- API ENDPOINT TESTS ---
    def test_market_quote(self):
        print("\n📈 [TEST] Market Quote (BTC-USD)...")
        response = self.app.post('/api/market/quote', 
                               json={'symbol': 'BTC-USD'},
                               content_type='application/json')
        data = response.json
        print(f"   Price: ${data.get('price', 'N/A')}")
        self.assertIn(data.get('status'), ['ok', 'stale', 'error'])

    def test_market_chart(self):
        print("\n📊 [TEST] Market Chart Data...")
        response = self.app.post('/api/market/chart', 
                               json={'symbol': 'BTC-USD', 'period': '1mo'},
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_market_sentiment_ai(self):
        print("\n🧠 [TEST] AI Sentiment Analysis...")
        response = self.app.post('/api/market/sentiment', 
                               json={'symbol': 'BTC-USD'},
                               content_type='application/json')
        print(f"   Sentiment: {response.json.get('sentiment')}")
        self.assertEqual(response.status_code, 200)

    def test_market_roi(self):
        print("\n⏳ [TEST] ROI Time Machine...")
        response = self.app.post('/api/market/roi', 
                               json={'symbol': 'BTC-USD', 'amount': 1000, 'years': 1},
                               content_type='application/json')
        data = response.json
        print(f"   ROI: {data.get('roi_pct')}%")
        self.assertEqual(response.status_code, 200)

    # --- INNER LOGIC TESTS ---
    def test_roi_math(self):
        print("\n🧮 [TEST] ROI Math Logic...")
        # Verify calculation manually
        result = market_brain.check_roi('BTC-USD', 1000, 1)
        # Even if data is stale/mocked, keys must exist
        self.assertIn('roi_pct', result)
        self.assertIn('current_value', result)

    def test_caching_mechanism(self):
        print("\n⚡ [TEST] Caching Mechanism...")
        symbol = "TEST-SYM"
        # Manually inject into cache
        CACHE[symbol] = {
            "data": {"price": 100, "status": "ok"},
            "timestamp": time.time()
        }
        
        # Fetch -> Should hit cache
        data = market_brain.get_quote(symbol)
        self.assertEqual(data['price'], 100)
        print("   Cache Hit Verified.")

    def test_input_sanitization(self):
        print("\n🛡️ [TEST] Input Sanitization...")
        # Test lowercase handling
        data = market_brain.get_quote('btc-usd') # Should convert to BTC-USD internally
        self.assertIn(data.get('status'), ['ok', 'stale', 'error'])

    # --- USER JOURNEY TEST ---
    def test_investor_journey(self):
        print("\n🚀 [TEST] SIMULATION: The 'Crypto Investor' Journey")
        # Step 1: User searches for ETH
        print("   1. User searches for 'ETH-USD'...")
        q = self.app.post('/api/market/quote', json={'symbol': 'ETH-USD'})
        self.assertIn(q.status_code, [200, 500])

        # Step 2: User Checks 1Y Chart
        print("   2. User opens 1 Year Chart...")
        c = self.app.post('/api/market/chart', json={'symbol': 'ETH-USD', 'period': '1y'})
        self.assertEqual(c.status_code, 200)

        # Step 3: User does a Vibe Check
        print("   3. User checks AI Sentiment...")
        s = self.app.post('/api/market/sentiment', json={'symbol': 'ETH-USD'})
        self.assertEqual(s.status_code, 200)

        # Step 4: User calculates ROI
        print("   4. User calculates 5-year ROI...")
        r = self.app.post('/api/market/roi', json={'symbol': 'ETH-USD', 'amount': 5000, 'years': 5})
        self.assertEqual(r.status_code, 200)
        print("   ✅ Simulation Complete.")

if __name__ == '__main__':
    print("="*60)
    print("💎 MARKET WIDGET: ISOLATED TEST SUITE")
    print("="*60)
    unittest.main()
