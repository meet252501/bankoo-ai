# 🧠 Bankoo AI - Your Ultimate Desktop AI Assistant

<div align="center">

![Bankoo AI](https://img.shields.io/badge/Bankoo-AI%20Assistant-00d4ff?style=for-the-badge&logo=robot&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=for-the-badge&logo=flask&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A comprehensive desktop AI assistant with 5 specialized agents, multi-language code execution, and enterprise-grade features.**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## ✨ Features

### 🤖 **5 Specialized AI Agents**

| Agent                | Icon | Description                                          |
| -------------------- | ---- | ---------------------------------------------------- |
| **Doc-Genius**       | 📚   | PDF RAG Engine - Analyze and query documents with AI |
| **Zenith Analytics** | 📊   | ML-powered predictions and data analysis             |
| **Cine-Match**       | 🎬   | Movie discovery and personalized recommendations     |
| **Market Insight**   | 📈   | Real-time global stock market analysis               |
| **Vision Lab**       | 👁️   | Hand tracking and gesture recognition                |

### 💻 **Multi-Language Code Execution**

Execute code in **15+ programming languages** with intelligent auto-detection:

- Python, JavaScript, TypeScript, Java, C++, C, C#
- Go, Rust, PHP, Ruby, Bash, SQL, HTML, R
- Built-in IDE with syntax highlighting, REPL, and terminal

### 🎯 **Enterprise Features**

- **Agent Nexus** - Multi-agent collaboration system
- **Smart Notes** - AI-powered note-taking with auto-organization
- **Web Scraper** - Advanced data extraction tool
- **Voice Input** - Multilingual voice commands (including Gujarati)
- **Telegram Integration** - Remote AI assistant access
- **Zenith Self-Correction** - AI learns from mistakes

### 🌍 **Global Market Support**

Track stocks from **ALL major exchanges**:

- 🇺🇸 US (NASDAQ, NYSE)
- 🇮🇳 India (NSE, BSE)
- 🇬🇧 UK (LSE)
- 🇩🇪 Germany (XETRA)
- 🇯🇵 Japan (TSE)
- 🇨🇳 China (Shanghai, Shenzhen)
- 🇭🇰 Hong Kong (HKEX)

---

## 🚀 Quick Start

> **For detailed instructions, see [QUICKSTART.md](QUICKSTART.md)**

### Option 1: Beautiful Web Installer (Recommended) ✨

**The easiest way to set up Bankoo!**

1. **Install dependencies** (one time):
   ```bash
   INSTALL_DEPENDENCIES.bat
   ```
2. **Launch the Installer**:

   ```bash
   cd installer && python setup_server.py
   ```

   _This opens a beautiful sci-fi wizard in your browser!_

3. **Follow the wizard**:
   - ✅ Auto-configured API keys (with "Get Key" buttons)
   - ✅ Select AI Agents & Modules
   - ✅ Choose Voice & Language
   - ✅ Click **Finish** to auto-save!

4. **Run Bankoo**:
   ```bash
   START_BANKOO.bat
   ```

### Option 2: Manual Installation

See [QUICKSTART.md](QUICKSTART.md) for full manual setup instructions.

3. **Configure API keys** (optional)

```bash
# Copy environment template
copy .env.example .env

# Edit .env and add your API keys
notepad .env
```

4. **Launch Bankoo**

```bash
START_BANKOO.bat
```

The UI will open automatically at `http://localhost:5000`

---

## 📖 Usage

### Basic Chat

1. Type your question in the input box
2. Press Enter or click Send
3. Bankoo responds with AI-powered answers

### Code Execution

1. Click the ⚡ lightning bolt icon
2. Write code in the CODE tab
3. Click ▶ Run to execute
4. View output in TERMINAL tab

### Voice Input

1. Click the 🎤 microphone icon
2. Speak your command
3. Bankoo transcribes and processes

### Agent Activation

1. Click an agent icon in the right sidebar
2. Upload files (PDF for Doc-Genius, CSV for Analytics)
3. Ask questions about your data

---

## 🔧 Configuration

### Required API Keys

Create a `.env` file with the following keys:

```env
# OpenAI (for GPT models)
OPENAI_API_KEY=your_openai_key_here

# Google Gemini (for vision and advanced reasoning)
GEMINI_API_KEY=your_gemini_key_here

# TMDB (for movie search - free tier available)
TMDB_API_KEY=your_tmdb_key_here

# Groq (for fast inference - free tier available)
GROQ_API_KEY=your_groq_key_here
```

### Getting API Keys

- **OpenAI**: https://platform.openai.com/api-keys
- **Google Gemini**: https://makersuite.google.com/app/apikey
- **TMDB**: https://www.themoviedb.org/settings/api
- **Groq**: https://console.groq.com/keys

---

## 🛠️ Tech Stack

### Backend

- **Flask** - Web framework
- **OpenAI API** - GPT models
- **Google Gemini** - Vision and reasoning
- **Groq** - Fast inference
- **LangChain** - RAG pipeline
- **FAISS** - Vector database
- **yfinance** - Stock market data

### Frontend

- **HTML5/CSS3** - Modern UI
- **JavaScript** - Interactive features
- **WebRTC** - Voice input
- **Fetch API** - Real-time updates

### AI Models

- **Llama 3.3 70B** - General conversation
- **Llama 3.1 8B** - Fast code generation
- **DeepSeek R1** - Deep reasoning
- **Gemini Pro** - Vision analysis

---

## 📚 Documentation

- [Feature Guide](FEATURE_GUIDE.md) - Detailed feature documentation
- [Runtime Setup](RUNTIME_SETUP_GUIDE.md) - Advanced configuration
- [Unified Architecture](UNIFIED_ARCHITECTURE.md) - System design
- [Agent Backend Solution](AGENT_BACKEND_SOLUTION.md) - Multi-agent system

---

## 🎯 Use Cases

### For Developers

- **Code Generation** - Write code in any language
- **Debugging** - AI-powered error analysis
- **Documentation** - Auto-generate docs from code
- **Learning** - Interactive coding tutor

### For Students

- **Research** - PDF analysis and summarization
- **Data Analysis** - ML predictions on datasets
- **Study Assistant** - Q&A on any topic
- **Project Help** - Code and concept explanations

### For Professionals

- **Market Analysis** - Real-time stock insights
- **Document Processing** - Extract info from PDFs
- **Automation** - Script generation
- **Decision Support** - AI-powered recommendations

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
4. **Push to the branch** (`git push origin feature/AmazingFeature`)
5. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/bankoo-ai.git

# Install dev dependencies
pip install -r requirements.txt

# Run in debug mode
DEBUG_START.bat
```

---

## 🐛 Troubleshooting

### Common Issues

**"No module named 'langchain'"**

```bash
INSTALL_DEPENDENCIES.bat
```

**Movies not working**

- Get free API key from https://www.themoviedb.org/
- Add to `.env` file

**Vision Lab not starting**

- Ensure webcam is connected
- Check camera permissions

**Code not executing**

- Click ⚡ lightning bolt to open Studio IDE
- Verify language is detected correctly

---

## 📊 Performance

- **Response Time**: < 2 seconds (with Groq)
- **Code Execution**: Real-time
- **Voice Recognition**: 95%+ accuracy
- **Supported Languages**: 15+ programming languages
- **Concurrent Users**: Up to 10 (local deployment)

---

## 🗺️ Roadmap

- [ ] Linux and macOS support
- [ ] Docker containerization
- [ ] Cloud deployment option
- [ ] Mobile app (Android/iOS)
- [ ] Plugin system for custom agents
- [ ] Multi-user collaboration
- [ ] Advanced vision models (YOLO, SAM)
- [ ] Local LLM support (Ollama integration)

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** - GPT models
- **Google** - Gemini API
- **Meta** - Llama models
- **Groq** - Fast inference
- **DeepSeek** - Reasoning models
- **LangChain** - RAG framework

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/bankoo-ai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/bankoo-ai/discussions)
- **Email**: your.email@example.com

---

## ⭐ Star History

If you find Bankoo AI helpful, please consider giving it a star! ⭐

---

<div align="center">

**Made with ❤️ by the Bankoo Team**

[⬆ Back to Top](#-bankoo-ai---your-ultimate-desktop-ai-assistant)

</div>
