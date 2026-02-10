# Zenith Optimizer (Agent-Lightning) Setup Guide

To enable self-improving capabilities in Bankoo, you need to set up the **Agent-Lightning** environment. Since this framework requires Linux, we recommend using **WSL (Windows Subsystem for Linux)**.

## 1. Prerequisites
- **WSL Installed**: If you haven't, run `wsl --install` in PowerShell.
- **Python 3.10+**: Inside WSL, ensure you have Python installed.
- **OpenAI API Key**: Agent-Lightning uses a teacher model (like GPT-4o) to optimize prompts.

## 2. Installation (Inside WSL)
Open your WSL terminal and run:

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install Agent-Lightning
pip install agentlightning

# --- OPTION A: Using Groq (Recommended & Fast) ---
export GROQ_API_KEY='your-groq-api-key'
export OPTIMIZER_MODEL='groq/llama-3.3-70b-versatile'

# --- OPTION B: Using OpenAI (Standard) ---
# export OPENAI_API_KEY='your-openai-api-key'
# export OPTIMIZER_MODEL='gpt-4o'
```

## 3. Running the Optimization Loop
Once you have interacted with Bankoo enough to generate some traces (check `logs/traces`), run the optimizer from the project root:

```bash
python3 zenith_optimizer.py
```

### What happens?
1. The script loads all your **Traces**.
2. It identifies interactions where Bankoo could have done better (Negative Rewards).
3. It sends these to the **APO (Automatic Prompt Optimizer)**.
4. It saves a new, improved system prompt in `logs/optimization/`.

## 4. Applying the Improvements
Open the latest `optimized_prompt_X.txt` in your logs and copy the content. You can then paste it into the `prompts` section of `assistant.py` or use it to update `language_logic.py`.

> [!TIP]
> Use this tool once a week to keep Bankoo at the cutting edge of performance!
