from app.llm import extract_with_llm
from app.database import (
    save_interaction,
    search_hcp as db_search_hcp,
)


# ==========================================================
# Helper
# ==========================================================

def build_summary(form):

    return f"""
✅ AI Analysis Complete

👨‍⚕️ HCP Name:
{form.get("hcpName","")}

📅 Date:
{form.get("date","")}

🕒 Time:
{form.get("time","")}

📞 Interaction Type:
{form.get("interactionType","")}

💊 Topics Discussed:
{form.get("topics","")}

📄 Materials Shared:
{form.get("materials","")}

🧪 Samples Distributed:
{form.get("samples","")}

😊 Overall HCP Sentiment:
{form.get("sentiment","")}

📝 Outcome:
{form.get("outcome","")}

📅 Follow-up:
{form.get("followUp","")}

-----------------------------------

✅ CRM Form Updated Successfully.
"""


# ==========================================================
# Tool 1 : Search HCP
# ==========================================================

def search_hcp(message):

    form = extract_with_llm(message)

    doctor = form["hcpName"]

    if not doctor:

        return {
            "reply": "Please provide an HCP name to search.",
            "tool": "search",
            "form": form,
        }

    result = db_search_hcp(doctor)

    if len(result) == 0:

        return {
            "reply": f"No previous interactions found for {doctor}.",
            "tool": "search",
            "form": form,
        }

    latest = result[0]

    return {
        "reply": f"""
🔍 Found {len(result)} interaction(s).

Latest Interaction

Doctor : {latest['hcp_name']}

Topics : {latest['topics']}

Sentiment : {latest['sentiment']}
""",
        "tool": "search",
        "form": form,
    }


# ==========================================================
# Tool 2 : Log Interaction
# ==========================================================

def log_interaction(message):

    form = extract_with_llm(message)

    interaction_id = save_interaction(form)

    return {
        "reply": build_summary(form)
        + f"\n\n🆔 Interaction ID : {interaction_id}",
        "tool": "log",
        "form": form,
    }


# ==========================================================
# Tool 3 : Edit Interaction
# ==========================================================

def edit_interaction(message):

    form = extract_with_llm(message)

    return {
        "reply": f"""
✏ Edit Interaction

This demo updates the CRM form.

(Database update can be connected using update_interaction()).

{build_summary(form)}
""",
        "tool": "edit",
        "form": form,
    }


# ==========================================================
# Tool 4 : Summarize
# ==========================================================

def summarize_interaction(message):

    form = extract_with_llm(message)

    return {
        "reply": f"""
📄 Interaction Summary

Doctor:
{form['hcpName']}

Interaction:
{form['interactionType']}

Topics:
{form['topics']}

Materials:
{form['materials']}

Samples:
{form['samples']}

Sentiment:
{form['sentiment']}

Outcome:
{form['outcome']}

Follow-up:
{form['followUp']}
""",
        "tool": "summary",
        "form": form,
    }


# ==========================================================
# Tool 5 : Follow-up
# ==========================================================

def suggest_followup(message=""):

    form = extract_with_llm(message)

    if form["sentiment"] == "Positive":

        follow = (
            "Schedule another meeting within 7 days."
        )

    elif form["sentiment"] == "Negative":

        follow = (
            "Reconnect after one month with updated material."
        )

    else:

        follow = (
            "Maintain regular communication."
        )

    form["followUp"] = follow

    return {
        "reply": f"""
📅 AI Follow-up Suggestion

{follow}
""",
        "tool": "followup",
        "form": form,
    }