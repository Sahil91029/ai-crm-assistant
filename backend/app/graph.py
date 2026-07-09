from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.tools import (
    search_hcp,
    log_interaction,
    edit_interaction,
    summarize_interaction,
    suggest_followup,
)


# =====================================================
# LangGraph State
# =====================================================

class CRMState(TypedDict):
    message: str
    tool: str
    result: dict


# =====================================================
# Node 1 : Understand User Intent
# =====================================================

def analyze(state: CRMState):

    message = state["message"].lower()

    if any(word in message for word in [
        "search",
        "find",
        "lookup",
        "doctor",
        "hcp",
    ]):
        state["tool"] = "search"

    elif any(word in message for word in [
        "edit",
        "update",
        "modify",
        "change",
    ]):
        state["tool"] = "edit"

    elif any(word in message for word in [
        "summary",
        "summarize",
        "summarise",
    ]):
        state["tool"] = "summary"

    elif any(word in message for word in [
        "follow",
        "follow-up",
        "next meeting",
    ]):
        state["tool"] = "followup"

    else:
        state["tool"] = "log"

    print("=" * 50)
    print("LangGraph Agent")
    print("Selected Tool :", state["tool"])
    print("=" * 50)

    return state


# =====================================================
# Node 2 : Execute Tool
# =====================================================

def execute(state: CRMState):

    tool = state["tool"]
    message = state["message"]

    if tool == "search":
        state["result"] = search_hcp(message)

    elif tool == "edit":
        state["result"] = edit_interaction(message)

    elif tool == "summary":
        state["result"] = summarize_interaction(message)

    elif tool == "followup":
        state["result"] = suggest_followup(message)

    else:
        state["result"] = log_interaction(message)

    return state


# =====================================================
# Build LangGraph
# =====================================================

builder = StateGraph(CRMState)

builder.add_node("Analyze", analyze)
builder.add_node("Execute Tool", execute)

builder.add_edge(START, "Analyze")
builder.add_edge("Analyze", "Execute Tool")
builder.add_edge("Execute Tool", END)

graph = builder.compile()


# =====================================================
# Public Function
# =====================================================

def run_graph(message: str):

    result = graph.invoke(
        {
            "message": message,
            "tool": "",
            "result": {},
        }
    )

    return result["result"]