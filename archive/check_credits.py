import os
import requests
import json
import config
from colorama import init, Fore, Style

# Initialize Colorama
init()

def print_header(title):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}=== {title} ==={Style.RESET_ALL}")

def print_status(name, status, details=""):
    color = Fore.GREEN if status == "PASS" or status == "ACTIVE" else Fore.RED
    if status == "WARN" or status == "FREE TIER": color = Fore.YELLOW
    
    print(f"{Fore.WHITE}{name:<20} {color}{status:<15} {Fore.WHITE}{details}")

def check_openrouter():
    """Check OpenRouter Credits & Info"""
    key = config.OPENROUTER_API_KEY
    if not key:
        print_status("OpenRouter", "MISSING", "No API Key found")
        return

    try:
        response = requests.get(
            "https://openrouter.ai/api/v1/auth/key",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            label = data.get('label', 'Unknown')
            usage = data.get('usage', 0)
            limit = data.get('limit')
            is_free = data.get('is_free_tier', False)
            
            status = "FREE TIER" if is_free else "ACTIVE"
            details = f"Label: {label} | Usage: ${usage:.4f}"
            if limit:
                details += f" / ${limit}"
            
            print_status("OpenRouter", status, details)
        elif response.status_code == 401:
            print_status("OpenRouter", "INVALID", "Key rejected")
        else:
            print_status("OpenRouter", "ERROR", f"Status {response.status_code}")
            
    except Exception as e:
        print_status("OpenRouter", "ERROR", str(e))

def check_llm_ping(provider, base_url, key, model):
    """Ping an LLM Provider with a minimal request"""
    if not key:
        print_status(provider, "MISSING", "No API Key found")
        return

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    # Handle specific provider headers/urls
    url = f"{base_url}/chat/completions"
    
    # Generic OpenAI-compatible payload
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Hi"}],
        "max_tokens": 1
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        
        if response.status_code == 200:
            print_status(provider, "ACTIVE", f"Ping success ({model})")
        elif response.status_code == 429:
            print_status(provider, "RATE LIMIT", "Out of credits / Quota exceeded")
        elif response.status_code == 401:
            print_status(provider, "INVALID", "Key rejected")
        elif response.status_code == 402:
            print_status(provider, "NO CREDIT", "Payment required")
        else:
            print_status(provider, "ERROR", f"Status {response.status_code}")
            
    except Exception as e:
        print_status(provider, "ERROR", str(e))

def main():
    print(f"{Fore.YELLOW}checking API Credits & Status...{Style.RESET_ALL}")
    
    check_openrouter()
    
    # GROQ
    check_llm_ping(
        "Groq", 
        "https://api.groq.com/openai/v1", 
        config.GROQ_API_KEY, 
        config.FAST_MODEL.split('/')[-1] if '/' in config.FAST_MODEL else config.FAST_MODEL
    )
    
    # Fireworks
    if hasattr(config, 'FIREWORKS_API_KEY') and config.FIREWORKS_API_KEY:
        check_llm_ping(
            "Fireworks",
            "https://api.fireworks.ai/inference/v1",
            config.FIREWORKS_API_KEY,
            "accounts/fireworks/models/llama-v3p3-70b-instruct"
        )
    else:
        print_status("Fireworks", "SKIPPED", "No Key Conf")

    # Cerebras
    if hasattr(config, 'CEREBRAS_API_KEY') and config.CEREBRAS_API_KEY:
        check_llm_ping(
            "Cerebras",
            "https://api.cerebras.ai/v1",
            config.CEREBRAS_API_KEY,
            "llama3.1-8b"
        )
    else:
        print_status("Cerebras", "SKIPPED", "No Key Conf")
        
    print("\nDone.\n")
    print(f"{Fore.CYAN}Reminder: OpenRouter 'Free Tier' has daily limits.{Style.RESET_ALL}")
    input("Press Enter to close...")

if __name__ == "__main__":
    main()
