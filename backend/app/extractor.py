import re
from datetime import datetime

# ---------------------------------------
# Word to Number
# ---------------------------------------

WORD_NUMBERS = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
    "ten": "10",
}

MONTHS = {
    "january": "01",
    "february": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "august": "08",
    "september": "09",
    "october": "10",
    "november": "11",
    "december": "12",
}

MATERIALS = [
    "brochure",
    "leaflet",
    "catalog",
    "flyer",
    "presentation",
    "pamphlet",
]

POSITIVE = [
    "interested",
    "happy",
    "positive",
    "good",
    "excellent",
    "agreed",
    "liked",
]

NEGATIVE = [
    "negative",
    "rejected",
    "declined",
    "not interested",
]

# ---------------------------------------
# Normalize speech text
# ---------------------------------------

def normalize(text):

    text = text.lower()

    text = text.replace("a.m.", "AM")
    text = text.replace("p.m.", "PM")
    text = text.replace("am", "AM")
    text = text.replace("pm", "PM")

    text = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", text)

    for word, number in WORD_NUMBERS.items():
        text = re.sub(rf"\b{word}\b", number, text)

    return text


# ---------------------------------------
# Parse Date
# ---------------------------------------

def extract_date(text):

    text = normalize(text)

    match = re.search(
        r"(\d{1,2})\s+([a-zA-Z]+)\s+(\d{4})",
        text,
    )

    if not match:
        return ""

    day = match.group(1).zfill(2)

    month = MONTHS.get(match.group(2).lower())

    year = match.group(3)

    if not month:
        return ""

    return f"{year}-{month}-{day}"


# ---------------------------------------
# Parse Time
# ---------------------------------------

def extract_time(text):

    text = normalize(text)

    match = re.search(
        r"(\d{1,2}):(\d{2})\s*(AM|PM)",
        text,
        re.I,
    )

    if match:

        return datetime.strptime(
            match.group(),
            "%I:%M %p",
        ).strftime("%H:%M")

    match = re.search(
        r"(\d{1,2})\s*(AM|PM)",
        text,
        re.I,
    )

    if match:

        return datetime.strptime(
            match.group(),
            "%I %p",
        ).strftime("%H:%M")

    return ""


# ---------------------------------------
# Main Extractor
# ---------------------------------------

def extract_information(message):

    text = normalize(message)

    form = {
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

    # Doctor

    doctor = re.search(
        r"dr\.?\s+[a-z]+",
        text,
        re.I,
    )

    if doctor:
        form["hcpName"] = doctor.group().title()

    # Interaction

    if "call" in text:
        form["interactionType"] = "Call"

    elif "email" in text:
        form["interactionType"] = "Email"

    else:
        form["interactionType"] = "Meeting"

    # Date

    form["date"] = extract_date(message)

    # Time

    form["time"] = extract_time(message)

    # Materials

    for material in MATERIALS:

        if material in text:
            form["materials"] = material.title()

    # Samples

    sample = re.search(
        r"(\d+)\s+samples?",
        text,
    )

    if sample:
        form["samples"] = sample.group(1)

    # Medicine names
    #
    # Extract words after discussed/discuss/discussed about

    topic = re.search(
        r"(?:discuss|discussed|about)\s+(.+?)(?:\.|,|and i|i shared|i gave|he was|$)",
        text,
    )

    if topic:
        form["topics"] = topic.group(1).title()

    # Sentiment

    if any(word in text for word in POSITIVE):

        form["sentiment"] = "Positive"

        form["outcome"] = "Doctor showed positive interest."

    elif any(word in text for word in NEGATIVE):

        form["sentiment"] = "Negative"

        form["outcome"] = "Doctor was not interested."

    # Follow-up

    if "follow" in text or "next week" in text:
        form["followUp"] = "Schedule follow-up meeting."

    return form