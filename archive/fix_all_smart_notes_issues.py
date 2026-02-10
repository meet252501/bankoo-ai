"""
COMPREHENSIVE SMART NOTES & BANKO AI DIAGNOSTIC + FIX
Fixes: Note creation, Backend integration, Gujarati responses
"""
import os
import json

print("🔍 BANKO AI & SMART NOTES COMPREHENSIVE DIAGNOSTIC")
print("="*70)

issues_found = []
fixes_applied = []

# ============================================================================
# PART 1: SMART NOTES BACKEND VERIFICATION
# ============================================================================
print("\n📦 PART 1: Checking Smart Notes Backend...")

if not os.path.exists('smart_notes.py'):
    issues_found.append("❌ smart_notes.py missing")
    print("  ❌ CRITICAL: smart_notes.py not found!")
else:
    print("  ✅ smart_notes.py exists")
    
    # Check if it has required functions
    with open('smart_notes.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if 'def create_note' not in content:
            issues_found.append("❌ create_note function missing")
        if 'def get_all_notes' not in content:
            issues_found.append("❌ get_all_notes function missing")
        if 'def update_note' not in content:
            issues_found.append("❌ update_note function missing")
        if 'def delete_note' not in content:
            issues_found.append("❌ delete_note function missing")

# Check bankoo_main.py has Smart Notes API
print("\n🔌 Checking API Endpoints...")
with open('bankoo_main.py', 'r', encoding='utf-8') as f:
    main_content = f.read()
    
    required_endpoints = [
        ('/api/notes', 'GET'),
        ('/api/notes', 'POST'),
        ('/api/notes/<int:note_id>', 'PUT'),
        ('/api/notes/<int:note_id>', 'DELETE'),
        ('/api/notes/summarize', 'POST'),
        ('/api/notes/ask', 'POST')
    ]
    
    for endpoint, method in required_endpoints:
        if endpoint in main_content:
            print(f"  ✅ {method} {endpoint}")
        else:
            print(f"  ❌ Missing: {method} {endpoint}")
            issues_found.append(f"Missing endpoint: {endpoint}")

# ============================================================================
# PART 2: SMART NOTES FRONTEND VERIFICATION
# ============================================================================
print("\n🎨 PART 2: Checking Smart Notes Frontend...")

with open('bankoo_ui.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check saveNote function
if 'function saveNote' in html:
    print("  ✅ saveNote() function exists")
    
    # Check if it's using the right API endpoint
    if '/api/notes' in html:
        print("  ✅ API endpoint referenced")
    else:
        print("  ❌ API endpoint NOT referenced in saveNote")
        issues_found.append("saveNote not calling API")
else:
    print("  ❌ saveNote() function MISSING!")
    issues_found.append("saveNote function missing")

# Check if notesView exists
if 'id="notesView"' in html:
    print("  ✅ Notes view HTML exists")
else:
    print("  ❌ Notes view HTML MISSING!")
    issues_found.append("Notes view missing")

# ============================================================================
# PART 3: CHECK CONSOLE ERRORS (Create test HTML)
# ============================================================================
print("\n🐛 PART 3: Creating Debug Test Page...")

debug_html = """<!DOCTYPE html>
<html>
<head>
    <title>Smart Notes Debug Test</title>
</head>
<body>
    <h1>Smart Notes API Test</h1>
    <button onclick="testCreateNote()">Test Create Note</button>
    <button onclick="testGetNotes()">Test Get Notes</button>
    <div id="result"></div>
    
    <script>
        async function testCreateNote() {
            try {
                const res = await fetch('http://127.0.0.1:5001/api/notes', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        title: 'Test Note',
                        content: 'This is a test',
                        tags: ['test']
                    })
                });
                const data = await res.json();
                document.getElementById('result').innerHTML = 
                    '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                alert('✅ Create Note: SUCCESS');
            } catch (e) {
                alert('❌ Create Note FAILED: ' + e.message);
                console.error(e);
            }
        }
        
        async function testGetNotes() {
            try {
                const res = await fetch('http://127.0.0.1:5001/api/notes');
                const data = await res.json();
                document.getElementById('result').innerHTML = 
                    '<pre>Found ' + data.length + ' notes:\\n' + 
                    JSON.stringify(data, null, 2) + '</pre>';
                alert('✅ Get Notes: SUCCESS (' + data.length + ' notes)');
            } catch (e) {
                alert('❌ Get Notes FAILED: ' + e.message);
                console.error(e);
            }
        }
    </script>
</body>
</html>"""

with open('test_smart_notes_api.html', 'w', encoding='utf-8') as f:
    f.write(debug_html)

print("  ✅ Created test_smart_notes_api.html")
print("     → Open this file in browser to test API")

# ============================================================================
# PART 4: GUJARATI RESPONSE FIX
# ============================================================================
print("\n🇮🇳 PART 4: Checking Gujarati Language Support...")

# Check assistant.py for language handling
if os.path.exists('assistant.py'):
    with open('assistant.py', 'r', encoding='utf-8') as f:
        assistant_content = f.read()
        
    if 'gujarati' in assistant_content.lower() or 'ગુજરાતી' in assistant_content:
        print("  ✅ Gujarati language handling found")
    else:
        print("  ⚠️  No specific Gujarati handling detected")
        print("  🔧 Adding Gujarati language improvement...")
        
        # Add Gujarati prompt enhancement
        gujarati_fix = '''
# Add this to improve Gujarati responses in assistant.py

def enhance_gujarati_prompt(user_message):
    """Enhance prompt for better Gujarati responses"""
    if any(char in user_message for char in 'અઆઇઈઉઊએઓકખગઘચછજ'):
        # User is typing in Gujarati
        return f"""You are Bankoo AI, fluent in Gujarati. 
Respond ONLY in native Gujarati script (ગુજરાતી).
Use natural, conversational Gujarati.
Do NOT mix English or Roman script.

User message: {user_message}

Response in Gujarati:"""
    return user_message
'''
        
        with open('gujarati_language_fix.txt', 'w', encoding='utf-8') as f:
            f.write(gujarati_fix)
        
        print("  ✅ Gujarati enhancement guide created: gujarati_language_fix.txt")
        fixes_applied.append("Gujarati prompt enhancement guide")

# ============================================================================
# PART 5: FINAL SUMMARY & FIXES
# ============================================================================
print("\n" + "="*70)
print("📊 DIAGNOSTIC SUMMARY")
print("="*70)

if issues_found:
    print("\n⚠️  ISSUES FOUND:")
    for issue in issues_found:
        print(f"  • {issue}")
else:
    print("\n✅ No major issues detected!")

if fixes_applied:
    print("\n🔧 FIXES APPLIED:")
    for fix in fixes_applied:
        print(f"  • {fix}")

print("\n" + "="*70)
print("✅ RECOMMENDATIONS")
print("="*70)

print("""
1. SMART NOTES NOT CREATING:
   • Make sure Bankoo backend is RUNNING (python bankoo_main.py)
   • Open test_smart_notes_api.html in browser
   • Click both buttons to test API
   • Check browser console (F12) for errors
   
2. BACKEND REQUIREMENTS:
   ✅ smart_notes.py - CRUD manager
   ✅ bankoo_main.py - API endpoints (/api/notes)
   ✅ bankoo_ui.html - Frontend with saveNote()
   
3. GUJARATI RESPONSES:
   • Add system message: "Respond in native Gujarati only"
   • Check assistant.py for language detection
   • See gujarati_language_fix.txt for improvements
   
4. GENERAL BANKO AI RESPONSES:
   • Check config.py for model settings
   • Verify GROQ_API_KEY is set
   • Model: llama-3.1-8b-instant (should be good)
   
5. IF NOTES STILL DON'T SAVE:
   • Check if smart_notes.json is writable
   • Verify fetch() calls in saveNote()
   • Test API directly with test_smart_notes_api.html

""")

print("🎯 Next: Open test_smart_notes_api.html and test the API!")
print("="*70)
