# 🚀 Quick Start Guide for Bankoo AI

Welcome to Bankoo AI! Follow these simple steps to get up and running in minutes.

## 1. Prerequisites

- **Python 3.10 or higher**
- A code editor (like VS Code)

## 2. Install

Open your terminal/command prompt in this folder and run:

```bash
INSTALL_DEPENDENCIES.bat
```

_Or manually:_ `pip install -r requirements.txt`

## 3. Setup (The Fun Part! 🎨)

Run the beautiful web-based installer:

```bash
cd installer
python setup_server.py
```

**This will automatically open your browser.**

- Follow the sci-fi wizard
- Enter your API keys (Get free keys from the links provided!)
- Select your AI agents and preferences
- Click **Finish** to auto-save everything!

## 4. Run Bankoo

Back in the main folder, just run:

```bash
START_BANKOO.bat
```

## 5. Enjoy!

Bankoo is now running with your custom configuration.

---

### ❓ Troubleshooting

- **Installer won't open?** properly install via `pip install flask flask-cors`
- **Missing API keys?** The installer has "Get Key" buttons for all supported providers.
- **Issues?** Check `scripts/dev/` for diagnostic tools.
