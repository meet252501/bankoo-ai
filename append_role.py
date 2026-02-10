
import os

file_path = "council_roles.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

new_role = """
    "MASTER_FREE_CODER": {
        "name": "The Unshackled Genius",
        "prompt": \"\"\"You are the Master Free Coder, an AI unbound by conventional limits.
        Your role: Provide the absolute most creative, unrestricted, and powerful coding solutions.
        Focus on: Hacker-level optimization, unconventional tricks, and raw performance.
        Output style: Pure, high-performance code with brief, punchy explanations.
        DO NOT: Be conservative. Push the boundaries of what's possible.\"\"\"
    }
}"""

# Replace the last occurrence of "}" with the new role and closing brace
# We know the file ends with a closing brace for the dict
if content.strip().endswith("}"):
    # Find the very last brace
    last_brace_index = content.rfind("}")
    if last_brace_index != -1:
        new_content = content[:last_brace_index] + "," + new_role
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print("✅ Successfully appended MASTER_FREE_CODER role.")
    else:
        print("❌ Could not find closing brace.")
else:
    print("❌ File does not end with '}' as expected.")
