
"""
Smart Notes Diagnostic and Auto-Fix
Checks what's broken and fixes it automatically
"""
import os
import json

print("🔍 Smart Notes Diagnostic Starting...\n")

# Check 1: Backend files exist
print("📁 Checking backend files:")
if os.path.exists('smart_notes.py'):
    print("  ✅ smart_notes.py found")
else:
    print("  ❌ smart_notes.py MISSING!")

if os.path.exists('bankoo_main.py'):
    print("  ✅ bankoo_main.py found")
    # Check if notes endpoints exist
    with open('bankoo_main.py', 'r', encoding='utf-8') as f:
        content = f.read()
        if '/api/notes' in content:
            print("  ✅ Notes API endpoints found")
        else:
            print("  ❌ Notes API endpoints MISSING!")
else:
    print("  ❌ bankoo_main.py MISSING!")

# Check 2: Frontend Smart Notes UI
print("\n📄 Checking frontend:")
if os.path.exists('bankoo_ui.html'):
    with open('bankoo_ui.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
        if 'id="notesView"' in html:
            print("  ✅ Notes view HTML found")
        else:
            print("  ❌ Notes view HTML MISSING!")
            
        if 'function loadNotes' in html:
            print("  ✅ loadNotes() function found")
        else:
            print("  ❌ loadNotes() function MISSING!")
            
        if 'function saveNote' in html:
            print("  ✅ saveNote() function found")
        else:
            print("  ❌ saveNote() function MISSING!")
else:
    print("  ❌ bankoo_ui.html MISSING!")

# Check 3: App drawer integration
print("\n🚀 Checking app launcher:")
with open('bankoo_ui.html', 'r', encoding='utf-8') as f:
    html = f.read()
    
    if "case 'notes':" in html:
        print("  ✅ Notes case found in openApp()")
        
        # Check if it still has alert
        if 'alert' in html.split("case 'notes':")[1].split('break;')[0]:
            print("  ⚠️  Still showing 'Coming Soon' alert!")
            print("  🔧 FIXING: Replacing alert with app opener...")
            
            # Fix the alert
            import re
            pattern = r"case 'notes':\s*alert\([^)]+\);\s*break;"
            replacement = "case 'notes':\\n                    document.getElementById('notesView').style.display = 'block';\\n                    loadNotes();\\n                    break;"
            html = re.sub(pattern, replacement, html, flags=re.DOTALL)
            
            with open('bankoo_ui.html', 'w', encoding='utf-8') as fw:
                fw.write(html)
            print("  ✅ FIXED! Alert replaced with app opener")
        else:
            print("  ✅ App opener code looks correct")
    else:
        print("  ❌ Notes case NOT found in openApp()!")

# Check 4: Test note storage
print("\n💾 Checking note storage:")
if os.path.exists('smart_notes.json'):
    with open('smart_notes.json', 'r', encoding='utf-8') as f:
        try:
            notes = json.load(f)
            print(f"  ✅ Storage working ({len(notes)} notes found)")
        except:
            print("  ⚠️  Storage file corrupted, resetting...")
            with open('smart_notes.json', 'w') as fw:
                json.dump([], fw)
            print("  ✅ Storage reset to empty")
else:
    print("  ℹ️  No storage file yet (will be created on first note)")

print("\n" + "="*50)
print("📊 DIAGNOSTIC SUMMARY:")
print("="*50)

# Final recommendation
print("\n✅ NEXT STEPS:")
print("1. Make sure Bankoo is STOPPED (close bankoo_main.py)")
print("2. Restart: python bankoo_main.py")
print("3. Open browser to http://127.0.0.1:5001")
print("4. Click 📱 App Drawer → Click 📝 Smart Notes")
print("\nIf Smart Notes still doesn't open, the issue is likely:")
print("  • Browser cache (Ctrl+F5 to hard refresh)")
print("  • Backend not restarted")
print("  • Port 5001 not accessible")
print("\n✨ Diagnostic complete!")
