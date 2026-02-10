# Bankoo AI - Feature Guide & Troubleshooting

## 🎯 Overview
Bankoo AI is a comprehensive desktop AI assistant with 5 specialized agents and multi-language code execution.

---

## 🤖 AI Agents

### 1. 📚 Doc-Genius (PDF RAG Engine)
**What it does:** Analyze and query PDF documents using AI
**How to use:** 
- Click the 📚 button in the right sidebar
- Upload a PDF file
- Ask questions about the document in the main chat

**Dependencies:** `langchain`, `PyPDF2`, `faiss-cpu`, `sentence-transformers`

### 2. 📊 Zenith Analytics (ML Predictions)
**What it does:** Predict student performance from CSV datasets
**How to use:**
- Click the 📊 button in the right sidebar
- Upload a CSV file with student data
- Get ML-powered predictions

**Dependencies:** `pandas`, `numpy`, `scikit-learn`

### 3. 🎬 Cine-Match (Movie Discovery)
**What it does:** Search movies and get personalized recommendations
**How to use:**
- Click the 🎬 button in the right sidebar
- Search for any movie by name
- View details, ratings, and similar movies

**API Key Required:** Get free API key from https://www.themoviedb.org/settings/api
- Add to `config.py`: `TMDB_API_KEY = "your_key_here"`

**Dependencies:** `tmdbv3api`, `requests`

### 4. 📈 Market Insight (Stock Analysis)
**What it does:** Real-time stock market data and analysis for **ALL global markets**
**How to use:**
- Click the 📈 button in the right sidebar
- Enter any stock ticker symbol:
  - **US Stocks:** AAPL, TSLA, MSFT, GOOGL
  - **Indian Stocks:** RELIANCE.NS, TCS.NS, INFY.NS (add .NS for NSE)
  - **European Stocks:** SAP.DE, ASML.AS (add country code)
  - **Chinese Stocks:** BABA, JD, BIDU

**Examples:**
- Apple (US): `AAPL`
- Reliance Industries (India): `RELIANCE.NS`
- Tata Consultancy Services (India): `TCS.BO` (Bombay Stock Exchange)
- Samsung (Korea): `005930.KS`

**Dependencies:** `yfinance` (supports global stock exchanges)

### 5. 👁️ Vision Lab (Hand Tracking)
**What it does:** Real-time hand tracking and gesture recognition
**How to use:**
- Click the 👁️ button in the right sidebar
- Click "Launch Vision Lab"
- A camera window will open showing hand landmarks
- Press ESC to stop

**Dependencies:** `opencv-python`, `mediapipe`
**Requires:** Working webcam

---

## ⚙️ Code Execution Engine

### Supported Programming Languages (15+)

| Language | File Extension | Auto-Detection |
|----------|---------------|----------------|
| Python | `.py` | `def`, `import`, `print(` |
| JavaScript | `.js` | `console.log`, `function`, `const` |
| TypeScript | `.ts` | `: string`, `: number`, `interface` |
| Java | `.java` | `public class`, `static void main` |
| C++ | `.cpp` | `#include`, `std::` |
| C | `.c` | `#include`, `int main` |
| C# | `.cs` | `using System`, `Console.WriteLine` |
| Go | `.go` | `package main`, `func main` |
| Rust | `.rs` | `fn main`, `println!` |
| PHP | `.php` | `<?php` |
| Ruby | `.rb` | `def`, `puts` |
| Bash | `.sh` | `#!/bin/bash`, `echo` |
| SQL | `.sql` | `SELECT`, `INSERT`, `CREATE TABLE` |
| HTML | `.html` | `<!DOCTYPE html>`, `<html>` |
| R | `.r` | `<-`, `library(` |

### How to Use Code Editor:
1. Click the lightning bolt ⚡ button (bottom input bar)
2. Studio IDE opens with:
   - **CODE Tab:** Write your code
   - **TERMINAL Tab:** View execution output
   - **REPL Tab:** Interactive Python shell
   - **PREVIEW Tab:** For HTML/web output

3. **Auto-Detection:** Just write code and click "Run" - Bankoo detects the language
4. **Manual Language:** Or specify in your prompt: "Write a Python function to..."

### Code Examples:

**Python:**
```python
def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)

print(factorial(5))  # Output: 120
```

**JavaScript:**
```javascript
const greet = (name) => {
    console.log(`Hello, ${name}!`);
}

greet("Bankoo");
```

**Java:**
```java
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello from Java!");
    }
}
```

---

## 🔧 Installation & Setup

### Quick Start (Missing Dependencies Fix):
1. **Run:** `INSTALL_DEPENDENCIES.bat`
2. Wait for installation (5-10 minutes)
3. **Launch:** `START_BANKOO.bat`

### API Keys (Optional but Recommended):

**TMDB (Movies):**
1. Sign up at https://www.themoviedb.org/
2. Go to Settings → API
3. Copy API Key (v3 auth)
4. Add to `config.py`: `TMDB_API_KEY = "your_key"`

---

## 🌍 International Stock Markets

Market Insight supports **ALL global stock exchanges** via Yahoo Finance:

### Stock Ticker Formats:

| Country | Exchange | Format | Example |
|---------|----------|--------|---------|
| USA | NASDAQ/NYSE | `SYMBOL` | `AAPL`, `TSLA` |
| India | NSE | `SYMBOL.NS` | `RELIANCE.NS`, `TCS.NS` |
| India | BSE | `SYMBOL.BO` | `RELIANCE.BO`, `INFY.BO` |
| UK | LSE | `SYMBOL.L` | `BP.L`, `HSBA.L` |
| Germany | XETRA | `SYMBOL.DE` | `SAP.DE`, `VOW3.DE` |
| Japan | TSE | `SYMBOL.T` | `7203.T` (Toyota) |
| China | Shanghai | `SYMBOL.SS` | `600519.SS` |
| Hong Kong | HKEX | `SYMBOL.HK` | `0700.HK` (Tencent) |

**Top Indian Stocks:**
- Reliance Industries: `RELIANCE.NS`
- Tata Consultancy: `TCS.NS`
- Infosys: `INFY.NS`
- HDFC Bank: `HDFCBANK.NS`
- Bharti Airtel: `BHARTIARTL.NS`

---

## ❌ Common Issues & Fixes

### 1. "No module named 'langchain'"
**Fix:** Run `INSTALL_DEPENDENCIES.bat`

### 2. Movies not working
**Fix:** 
- Run `INSTALL_DEPENDENCIES.bat` (installs tmdbv3api)
- Add TMDB API key to `config.py`

### 3. Vision Lab not working
**Fix:**
- Run `INSTALL_DEPENDENCIES.bat` (installs opencv + mediapipe)
- Ensure webcam is connected and accessible

### 4. Code not executing
**Check:**
- Click the ⚡ lightning bolt to open Studio IDE
- Write code in CODE tab
- Click "▶ Run" button
- View output in TERMINAL tab

### 5. Market only shows American stocks
**Not a bug!** You can search ANY global stock:
- Just add the correct suffix (`.NS` for India, `.L` for UK, etc.)
- See the table above for formats

---

## 💡 Pro Tips

1. **Voice Input:** Click the microphone 🎤 button to speak to Bankoo
2. **Gujarati Support:** Bankoo understands and responds in Gujarati
3. **Studio IDE Shortcuts:**
   - `Alt + S` - Toggle Studio
   - `Alt + V` - Toggle Voice
   - `Alt + H` - Toggle History
4. **Code Selection:** Select specific code and click Run for bit-by-bit execution
5. **Interactive REPL:** Use the Python REPL tab for quick calculations

---

## 🚀 Performance

- **Primary Model:** Llama 3.3 70B (General conversation)
- **Coding Model:** Llama 3.1 8B (Fast code generation)
- **Reasoning Model:** DeepSeek R1 (Deep logic tasks)
- **Code Reviewer:** DeepSeek R1 (Code analysis and suggestions)

---

**Need Help?** Check the console output when running `START_BANKOO.bat` for specific error messages.
