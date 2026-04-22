import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Use ENV variable (SAFE)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PROMPT_TEMPLATE = """
Extract the following information and return ONLY valid JSON.

Keys required:
summary, entities, sentiment, questions

Text:
{chunk}
"""

def call_llm(chunk):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": PROMPT_TEMPLATE.format(chunk=chunk)}
            ],
            temperature=0
        )
        print("RAW RESPONSE:", response)
        # 🔥 SAFE extraction (no crash)
        if hasattr(response, "choices") and len(response.choices) > 0:
            choice = response.choices[0]

            if hasattr(choice, "message") and hasattr(choice.message, "content"):
                return choice.message.content

        print("⚠️ Unexpected response format:", response)
        return None

    except Exception as e:
        print("❌ LLM call failed:", e)
        return None