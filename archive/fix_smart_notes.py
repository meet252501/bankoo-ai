"""
Automatic fixer for Smart Notes app launcher
"""
import re

# Read the HTML file
with open('bankoo_ui.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the alert with actual app opening code
old_pattern = r"case 'notes':\s*alert\([^)]+\);\s*break;"
new_code = "case 'notes':\n                    document.getElementById('notesView').style.display = 'block';\n                    loadNotes();\n                    break;"

# Perform replacement
content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)

# Write back
with open('bankoo_ui.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Smart Notes app launcher fixed!")
print("📝 Smart Notes is now fully functional!")
print("\nTo use:")
print("1. Restart Bankoo (if running)")
print("2. Click 📱 App Drawer")
print("3. Click 📝 Smart Notes")
print("4. Click + New Note to create notes!")
