# 🚀 Bankoo AI - Beautiful Web Installer

## How to Use

### Step 1: Install Flask

```bash
pip install flask flask-cors
```

### Step 2: Run the Installer

```bash
cd Desktop/github/installer
python setup_server.py
```

### Step 3: Configure Bankoo

- Browser opens automatically to http://localhost:5555/
- Beautiful HTML installer appears
- Click through pages:
  1. Welcome
  2. API Keys (paste your keys)
  3. AI Agents (select which to enable)
  4. Brain Modules (select features)
  5. Voice (choose language)
  6. Preferences (theme, models)
  7. Complete (save!)

### Step 4: Done!

- Configuration automatically saved to:
  - `.env` - Your API keys
  - `installer_config.json` - Full config
  - `config_updates.py` - Code to copy into config.py

---

## What It Does

**Frontend:** Beautiful HTML with sci-fi design

- Animations, gradients, glassmorphism
- Professional UX
- "Get Key" buttons open provider websites

**Backend:** Flask Python server

- Receives configuration from HTML
- Saves to `.env` file
- Generates config files
- No manual editing needed!

---

## Files Created

### `.env`

```
GROQ_API_KEY=gsk_xxx...
CEREBRAS_API_KEY=csk_xxx...
GEMINI_API_KEY=AIza_xxx...
```

### `installer_config.json`

Full configuration in JSON format

### `config_updates.py`

Python code with your settings - copy into `config.py`

---

## Benefits

✅ Beautiful design (HTML)
✅ Actually functional (Flask)
✅ Auto-saves everything
✅ No coding required for users
✅ Professional experience

**Best of both worlds!** 🎉
