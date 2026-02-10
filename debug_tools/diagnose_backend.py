import sys
import os
import json
import traceback

project_path = r"C:\Users\Meet Sutariya\Desktop\final banko.ai"
sys.path.append(project_path)
os.chdir(project_path)

print("🔍 Debugging Backend Integrations...")
try:
    import api_hub
    
    # 1. Test Analytics (Performance Prediction)
    print("\n--- Testing Zenith Analytics (Student Prediction) ---")
    mock_student = {
        "gender": "female",
        "race_ethnicity": "group B",
        "parental_level_of_education": "bachelor's degree",
        "lunch": "standard",
        "test_preparation_course": "completed",
        "reading_score": 72,
        "writing_score": 74
    }
    pred = api_hub.analytics_brain.predict_performance(mock_student)
    print(f"Prediction Result: {pred}")
    if "CatBoost Model" in str(pred.get('confidence', '')):
        print("✅ SUCCESS: Real CatBoost Model is responding.")
    else:
        print("⚠️ WARNING: Fallback Logic is active (Model not loading).")

    # 2. Test Movies (Offline Recommender)
    print("\n--- Testing Cine-Match (Offline Recs) ---")
    # Using a known movie title relative to the dataset logic
    recs = api_hub.movie_brain.recommend_by_title("Avatar")
    print(f"Recommendation Result: {recs[:100]}...")
    if "Recommended based on content" in str(recs):
        print("✅ SUCCESS: Offline NLP Recommender is responding.")
    else:
        print("⚠️ WARNING: Offline Recs failed.")

    # 3. Test Market (Live Data)
    print("\n--- Testing Market Insight (Live Data) ---")
    stock = api_hub.market_brain.get_stock_summary("TSLA")
    print(f"Stock Result: {str(stock)[:100]}...")
    if isinstance(stock, dict) and 'name' in stock:
         print("✅ SUCCESS: Live Market Data is responding.")
    else:
         print("⚠️ WARNING: Market API failed.")

    # 4. Test Doc-Genius (Logic Check)
    print("\n--- Testing Doc-Genius (Logic) ---")
    status = api_hub.doc_brain.query("What is this?")
    print(f"Query Result: {status}")
    if "No document loaded" in status:
        print("✅ SUCCESS: Doc-Genius Logic is active (waiting for file).")
    else:
        print("⚠️ WARNING: Unexpected Doc-Genius behavior.")

except Exception:
    print("\n❌ CRITICAL BACKEND ERROR:")
    traceback.print_exc()
