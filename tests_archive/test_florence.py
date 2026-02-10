"""
Test script for Florence-2 Vision Module
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("🧪 FLORENCE-2 VISION TEST")
print("=" * 60)

try:
    from vision_florence import vision_engine
    print("✅ vision_florence module imported successfully")
except Exception as e:
    print(f"❌ Failed to import vision_florence: {e}")
    sys.exit(1)

try:
    print("\n📸 Taking screenshot and analyzing...")
    result = vision_engine.analyze(prompt="<MORE_DETAILED_CAPTION>")
    
    print("\n🎯 RESULT:")
    print("-" * 60)
    if isinstance(result, dict):
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print(result)
    print("-" * 60)
    
    print("\n✅ Florence-2 Vision Test PASSED!")
    
except Exception as e:
    print(f"\n❌ Test FAILED: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
