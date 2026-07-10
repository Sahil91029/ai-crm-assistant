import json
import os
import re

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.extractor import extract_information

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if API_KEY:
    client = genai.Client(api_key=API_KEY)


PROMPT = """
You are an AI CRM assistant.

Extract CRM information from the user's interaction.

Return ONLY valid JSON.

Never explain.

Never use markdown.

Never use ```json.

Fields:

{
  "hcpName":"",
  "interactionType":"",
  "date":"",
  "time":"",
  "attendees":"",
  "topics":"",
  "materials":"",
  "samples":"",
  "sentiment":"",
  "outcome":"",
  "followUp":""
}

Rules

Doctor names:
Return full name.

Interaction Type:
Meeting
Call
Email

Date:
YYYY-MM-DD

Time:
24-hour format

Examples

3:30 PM

becomes

15:30

Samples

Only number.

Materials

Examples

Brochure
Leaflet
Presentation

Sentiment

Positive
Neutral
Negative

Return JSON only.

User Interaction:

"""


DEFAULT_RESPONSE = {
    "hcpName": "",
    "interactionType": "Meeting",
    "date": "",
    "time": "",
    "attendees": "",
    "topics": "",
    "materials": "",
    "samples": "",
    "sentiment": "Neutral",
    "outcome": "",
    "followUp": "",
}


def clean_json(text):

    text = text.strip()

    text = text.replace("```json", "")

    text = text.replace("```", "")

    match = re.search(r"\{.*\}", text, re.S)

    if match:

        return match.group()

    return text


def merge_defaults(data):

    result = DEFAULT_RESPONSE.copy()

    result.update(data)

    return result

def extract_with_llm(message: str):

    # If Gemini is not configured,
    # fallback to local extractor.

    if client is None:
        print("⚠ Gemini API Key not found. Using fallback extractor.")
        return extract_information(message)

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=PROMPT + message,
            config=types.GenerateContentConfig(
                temperature=0.0,
                max_output_tokens=512,
            ),
        )

        text = response.text

        cleaned = clean_json(text)

        data = json.loads(cleaned)

        return merge_defaults(data)

    except json.JSONDecodeError as e:

        print("JSON Parse Error:", e)

        print("Gemini Response:", text)

        return extract_information(message)

    except Exception as e:

        print("Gemini Error:", e)

        return extract_information(message)