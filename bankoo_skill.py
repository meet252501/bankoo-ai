import sys
import requests
import json

def main():
    if len(sys.argv) < 2:
        print("Usage: python bankoo_skill.py <message>")
        return

    message = sys.argv[1]
    url = "http://127.0.0.1:8000/api/bridge/telegram"
    
    try:
        response = requests.post(url, json={"message": message})
        if response.status_code == 200:
            print(f"Bankoo Pro received: {message}")
            print("\nAI Response:")
            print(response.json().get("response", "No response from Bankoo."))
        else:
            print(f"Error: Bankoo API returned {response.status_code}")
    except Exception as e:
        print(f"Failed to connect to Bankoo: {str(e)}")

if __name__ == "__main__":
    main()
