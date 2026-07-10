import re
from datetime import datetime

# ==========================================================
# WORD TO NUMBER
# ==========================================================

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
    "eleven": "11",
    "twelve": "12",
    "thirteen": "13",
    "fourteen": "14",
    "fifteen": "15",
    "sixteen": "16",
    "seventeen": "17",
    "eighteen": "18",
    "nineteen": "19",
    "twenty": "20",
}

# ==========================================================
# MONTHS
# ==========================================================

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

# ==========================================================
# MATERIALS
# ==========================================================

MATERIALS = [
    "brochure",
    "leaflet",
    "catalog",
    "pamphlet",
    "presentation",
    "flyer",
    "visual aid",
    "sample kit",
]

# ==========================================================
# POSITIVE
# ==========================================================

POSITIVE = [
    "interested",
    "positive",
    "happy",
    "good",
    "excellent",
    "agreed",
    "liked",
    "satisfied",
    "accepted",
]

NEGATIVE = [
    "negative",
    "declined",
    "rejected",
    "not interested",
    "angry",
    "poor",
]

# ==========================================================
# NORMALIZE SPEECH
# ==========================================================

def normalize(text):

    text = text.lower()

    text = text.replace("doctor", "dr")

    text = text.replace("dr.", "dr")

    text = text.replace("a.m.", " am ")

    text = text.replace("p.m.", " pm ")

    text = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", text)

    for word, number in WORD_NUMBERS.items():
        text = re.sub(rf"\b{word}\b", number, text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()

# ==========================================================
# DATE
# ==========================================================

def extract_date(text):

    text = normalize(text)

    # 13 July 2026

    match = re.search(
        r"(\d{1,2})\s+([a-z]+)\s+(\d{4})",
        text,
    )

    if match:

        day = match.group(1).zfill(2)

        month = MONTHS.get(match.group(2))

        year = match.group(3)

        if month:
            return f"{year}-{month}-{day}"

    # 2026-07-13

    match = re.search(
        r"(\d{4})-(\d{2})-(\d{2})",
        text,
    )

    if match:
        return match.group()

    return ""

# ==========================================================
# TIME
# ==========================================================

def extract_time(text):

    text = normalize(text)

    # 3:30 PM

    match = re.search(
        r"(\d{1,2}):(\d{2})\s*(am|pm)",
        text,
    )

    if match:

        return datetime.strptime(
            match.group(),
            "%I:%M %p",
        ).strftime("%H:%M")

    # 3 PM

    match = re.search(
        r"(\d{1,2})\s*(am|pm)",
        text,
    )

    if match:

        return datetime.strptime(
            match.group(),
            "%I %p",
        ).strftime("%H:%M")

    # 15:30

    match = re.search(
        r"\b([01]?\d|2[0-3]):([0-5]\d)\b",
        text,
    )

    if match:
        return match.group()

    return ""

# ==========================================================
# HCP NAME
# ==========================================================

def extract_hcp(text):
    text = normalize(text)

    match = re.search(
        r"\bdr\s+(.+?)(?=\s+(?:on|at|with|about|regarding|discussed|shared|gave|met|visited|called|email|phone|today|yesterday|tomorrow|next)\b|$)",
        text,
        re.IGNORECASE,
    )

    if not match:
        return ""

    name = " ".join(word.capitalize() for word in match.group(1).split())

    return f"Dr {name}"


# ==========================================================
# MATERIALS
# ==========================================================

def extract_material(text):

    text = normalize(text)

    for material in MATERIALS:
        if material in text:
            return material.title()

    return ""


# ==========================================================
# SAMPLES
# ==========================================================

def extract_samples(text):

    text = normalize(text)

    match = re.search(
        r"(\d+)\s+samples?",
        text,
    )

    if match:
        return match.group(1)

    return ""


# ==========================================================
# TOPICS / MEDICINES
# ==========================================================

def extract_topics(text):

    text = normalize(text)

    patterns = [
        r"(?:discussed|discuss|about)\s+(.+?)(?:\.|,| and | i | we |$)",
        r"(?:explained|presented)\s+(.+?)(?:\.|,| and | i | we |$)",
        r"(?:regarding)\s+(.+?)(?:\.|,| and | i | we |$)",
    ]

    for pattern in patterns:

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).title().strip()

    return ""


# ==========================================================
# SENTIMENT
# ==========================================================

def extract_sentiment(text):

    text = normalize(text)

    for word in NEGATIVE:
        if word in text:
            return (
                "Negative",
                "Doctor was not interested."
            )

    for word in POSITIVE:
        if word in text:
            return (
                "Positive",
                "Doctor showed positive interest."
            )

    return (
        "Neutral",
        ""
    )


# ==========================================================
# FOLLOW UP
# ==========================================================

def extract_followup(text):

    text = normalize(text)

    if "tomorrow" in text:
        return "Follow up tomorrow."

    if "next week" in text:
        return "Follow up next week."

    if "next month" in text:
        return "Follow up next month."

    if "follow up" in text:
        return "Schedule follow-up."

    if "follow-up" in text:
        return "Schedule follow-up."

    return ""

# ==========================================================
# MAIN EXTRACTOR
# ==========================================================

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

    # --------------------------------------------------
    # HCP Name
    # --------------------------------------------------

    form["hcpName"] = extract_hcp(message)

    # --------------------------------------------------
    # Interaction Type
    # --------------------------------------------------

    if any(word in text for word in ["call", "called", "phone"]):
        form["interactionType"] = "Call"

    elif any(word in text for word in ["email", "mail", "emailed"]):
        form["interactionType"] = "Email"

    else:
        form["interactionType"] = "Meeting"

    # --------------------------------------------------
    # Date & Time
    # --------------------------------------------------

    form["date"] = extract_date(message)
    form["time"] = extract_time(message)

    # --------------------------------------------------
    # Topics
    # --------------------------------------------------

    form["topics"] = extract_topics(message)

    # --------------------------------------------------
    # Materials
    # --------------------------------------------------

    form["materials"] = extract_material(message)

    # --------------------------------------------------
    # Samples
    # --------------------------------------------------

    form["samples"] = extract_samples(message)

    # --------------------------------------------------
    # Sentiment & Outcome
    # --------------------------------------------------

    sentiment, outcome = extract_sentiment(message)

    form["sentiment"] = sentiment
    form["outcome"] = outcome

    # --------------------------------------------------
    # Follow Up
    # --------------------------------------------------

    form["followUp"] = extract_followup(message)

    # --------------------------------------------------
    # Default Outcome
    # --------------------------------------------------

    if not form["outcome"]:
        form["outcome"] = (
            f"{form['interactionType']} logged successfully."
        )

    return form