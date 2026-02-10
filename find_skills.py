import os
import sys
import yaml

# Target essentials list from user
targets = [
    "github", "homebrew", "pm2", "tmux", "shell", "file-search", "apple", 
    "todoist", "calendar", "linear", "clickup", "things", 
    "kubectl", "docker", "vercel", "tailscale", "proxmox", 
    "tavily", "exa", "brave", "playwright", 
    "spotify", "veo", "eleven", "youtube", 
    "ynab", "whoop", "crypto"
]

def find_skills():
    skills_dir = os.path.join(os.path.dirname(__file__), "moltbot_skills")
    matches = {t: [] for t in targets}
    
    print(f"Scanning {skills_dir}...")
    
    for root, dirs, files in os.walk(skills_dir):
        if 'SKILL.md' in files:
            path = os.path.join(root, 'SKILL.md')
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                parts = content.split('---\n', 2)
                if len(parts) >= 2:
                    meta = yaml.safe_load(parts[1])
                    name = meta.get('name', '')
                    
                    # Check against targets
                    for t in targets:
                        if t in name.lower():
                            matches[t].append(name)
            except:
                pass

    print("\n--- MATCHES ---")
    for t, found in matches.items():
        print(f"{t}: {found}")

if __name__ == "__main__":
    find_skills()
