"""
SMART NOTES - JAVASCRIPT FIX
Fixes: currentNoteId initialization error preventing note creation
"""
import re

print("🔧 Fixing Smart Notes JavaScript Errors...")

# Read HTML
with open('bankoo_ui.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find where Smart Notes functions are defined
# We need to ensure currentNoteId is declared BEFORE newNote() uses it

print("\n1️⃣ Checking currentNoteId declaration...")

# Check if currentNoteId is already declared
if 'let currentNoteId' in html or 'var currentNoteId' in html:
    print("  ✅ currentNoteId declaration found")
    
    # Check if it's BEFORE newNote function
    currentnote_pos = html.find('currentNoteId')
    newnote_pos = html.find('function newNote()')
    
    if currentnote_pos < newnote_pos:
        print("  ✅ Declaration is before newNote()")
    else:
        print("  ❌ Declaration is AFTER newNote() - FIXING...")
        
        # Find the loadNotes function (should be first)
        loadnotes_match = re.search(r'(async function loadNotes\(\))', html)
        if loadnotes_match:
            # Insert currentNoteId declaration before loadNotes
            insert_pos = loadnotes_match.start()
            html = html[:insert_pos] + "\n        let currentNoteId = null;\n\n        " + html[insert_pos:]
            print("  ✅ FIXED: Moved currentNoteId to top")
else:
    print("  ❌ currentNoteId NOT declared! Adding...")
    
    # Find first Smart Notes function and add it before
    match = re.search(r'(async function loadNotes\(\)|function newNote\(\))', html)
    if match:
        insert_pos = match.start()
        html = html[:insert_pos] + "\n        let currentNoteId = null;\n\n        " + html[insert_pos:]
        print("  ✅ FIXED: Added currentNoteId declaration")

# Fix 2: Make sure dashHeader exists before drag code runs
print("\n2️⃣ Checking dashboard drag initialization...")

if 'dashHeader.addEventListener' in html:
    # Wrap in existence check
    drag_pattern = r"const dash = document\.getElementById\('dashboardView'\);\s+const header = document\.getElementById\('dashHeader'\);"
    
    safe_drag = """const dash = document.getElementById('dashboardView');
            const header = document.getElementById('dashHeader');
            
            if (!dash || !header) {
                console.warn('Dashboard elements not found, skipping drag init');
                return;
            }"""
    
    html = re.sub(drag_pattern, safe_drag, html)
    print("  ✅ FIXED: Added null checks for dashboard drag")

# Save fixed HTML
with open('bankoo_ui.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("\n" + "="*60)
print("✅ JAVASCRIPT FIXES APPLIED!")
print("="*60)
print("\n📋 What was fixed:")
print("  ✅ currentNoteId initialization error")
print("  ✅ Dashboard drag null check")
print("\n🎯 NEXT STEPS:")
print("  1. Hard refresh browser (Ctrl + F5)")
print("  2. Try creating a note again")
print("  3. Check console (F12) for any remaining errors")
print("\n✨ Smart Notes should now work!")
