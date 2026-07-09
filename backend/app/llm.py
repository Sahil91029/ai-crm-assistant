import os

from app.extractor import extract_information

try:
    from groq import Groq
except ImportError:
    Groq = None


def extract_with_llm(message: str):

    api_key = os.getenv("GROQ_API_KEY")

    if api_key and Groq:

        client = Groq(api_key=api_key)

        prompt = f"""
Extract CRM information from the text.

Return ONLY JSON.

Fields:

hcpName
interactionType
date
time
attendees
topics
materials
samples
sentiment
outcome
followUp

Text:

{message}
"""

        try:

            response = client.chat.completions.create(
                model="gemma2-9b-it",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0,
            )

            import json

            return json.loads(
                response.choices[0].message.content
            )

        except Exception:

            pass

    # -----------------------------
    # Fallback
    # -----------------------------

    return extract_information(message)