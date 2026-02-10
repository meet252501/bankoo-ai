
import os
from openai import OpenAI
import config

try:
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=config.GROQ_API_KEY
    )

    print("📡 Pinging Groq (Gemma 2)...")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Are you free to use?",
            }
        ],
        model="gemma2-9b-it",
    )

    print("✅ Success! Response:")
    print(chat_completion.choices[0].message.content)

except Exception as e:
    print(f"❌ Error: {e}")
