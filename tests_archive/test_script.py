import requests
import json
import time

BASE_URL = "http://127.0.0.1:5001/api/run_code"

LANGUAGES = [
    ("python", "print('Python Ready')"),
    ("javascript", "console.log('JS Ready');"),
    ("typescript", "console.log('TS Ready');"),
    ("bash", "echo 'Bash Ready'"),
    ("go", "package main\nimport \"fmt\"\nfunc main() { fmt.Println(\"Go Ready\") }"),
    ("rust", "fn main() { println!(\"Rust Ready\"); }"),
    ("c++", "#include <iostream>\nint main() { std::cout << \"CPP Ready\"; return 0; }"),
    ("java", "public class Main { public static void main(String[] args) { System.out.println(\"Java Ready\"); } }"),
    ("csharp", "using System;\nclass Program { static void Main() { Console.WriteLine(\"CSharp Ready\"); } }"),
    ("php", "<?php echo 'PHP Ready'; ?>"),
    ("ruby", "puts 'Ruby Ready'"),
    ("sql", "CREATE TABLE test(t text); INSERT INTO test VALUES('SQL Ready'); SELECT * FROM test;"),
    ("c", "#include <stdio.h>\nint main() { printf(\"C Ready\"); return 0; }"),
]

print(f"⚡ Testing {len(LANGUAGES)} Languages on Bankoo IDE...\n")
print(f"{'LANGUAGE':<12} | {'STATUS':<10} | {'OUTPUT':<30}")
print("-" * 60)

passed = 0
failed = 0

for lang, code in LANGUAGES:
    try:
        # Note: frontend sends 'lang' detected from code
        # But we send explicit lang to force backend routing test
        payload = {"code": code, "lang": lang}
        
        response = requests.post(BASE_URL, json=payload, timeout=20)
        
        if response.status_code == 200:
            data = response.json()
            output = data.get('output', '').strip()
            
            # Check success (based on output containing expected string)
            # SQL output includes headers, so check inclusivity
            expected_key = "Ready"
            if expected_key in output:
                print(f"{lang:<12} | ✅ PASS     | {output[:30].replace(chr(10), ' ')}")
                passed += 1
            else:
                print(f"{lang:<12} | ❌ FAIL     | Output: {output[:30]}")
                failed += 1
        else:
            print(f"{lang:<12} | ❌ ERROR    | HTTP {response.status_code}")
            failed += 1
            
    except Exception as e:
        print(f"{lang:<12} | ❌ EXCEPTION| {str(e)[:30]}")
        failed += 1

print("-" * 60)
print(f"Completed. Passed: {passed}/{len(LANGUAGES)}")
if failed == 0:
    print("\n✅ ALL LANGUAGES OPERATIONAL")
else:
    print(f"\n⚠️  {failed} LANGUAGES FAILED (Check Piston/Internet?)")
