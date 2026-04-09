from __future__ import annotations

from typing import Any, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from app.models.schemas import Phase, RoadmapRequest, RoadmapResponse
from app.services.llm import llm_service
from app.services.templates import select_blueprint


class RoadmapState(TypedDict, total=False):
    request: dict[str, Any]
    normalized_goal: str
    blueprint: dict[str, Any]
    planning_context: dict[str, Any]
    draft_plan: dict[str, Any]
    validated_plan: dict[str, Any]
    final_output: dict[str, Any]


checkpointer = MemorySaver()


def intake_node(state: RoadmapState) -> RoadmapState:
    request = state["request"]
    goal = request["goal"].strip()
    goal_type = request.get("goal_type") or "general"
    blueprint = select_blueprint(goal_type)
    return {
        "normalized_goal": goal,
        "blueprint": blueprint,
        "planning_context": {
            "goal": goal,
            "goal_type": goal_type,
            "profile": request["profile"],
            "focus": blueprint["focus"],
            "default_tools": blueprint["tools"],
        },
    }


def planner_node(state: RoadmapState) -> RoadmapState:
    ctx = state["planning_context"]
    profile = ctx["profile"]

    fallback = {
        "title": f"Roadmap for {ctx['goal']}",
        "summary": f"A phase-wise execution roadmap for {ctx['goal']} tailored to a {profile['experience_level']} founder.",
        "readiness_score": 68 if profile["technical_background"] else 56,
        "execution_mode": "lean-mvp",
        "tools_needed": list(dict.fromkeys(ctx["default_tools"] + profile.get("current_skills", [])))[:8],
        "next_7_days": [
            "Refine the problem statement and define one target user segment.",
            "Interview at least 5 potential users.",
            "Write a one-page MVP scope with only core outcomes.",
        ],
        "next_30_days": [
            "Build a clickable prototype or lightweight MVP.",
            "Validate pricing and willingness to pay with early users.",
            "Set up landing page, analytics, and feedback loop.",
        ],
        "next_90_days": [
            "Launch the MVP to a narrow audience and measure retention.",
            "Add the highest-impact workflow automation.",
            "Iterate based on user pain points and conversion data.",
        ],
        "phases": [
            {
                "phase_title": "Phase 1 — Discovery & Positioning",
                "objective": "Validate the problem, target user, and value proposition.",
                "duration": "Week 1-2",
                "key_tasks": [
                    "Write problem hypothesis",
                    "Choose niche segment",
                    "Run customer interviews",
                    "Map competitors and alternatives",
                ],
                "deliverables": ["Problem brief", "User persona", "Competitor snapshot"],
                "success_metrics": ["5-10 interviews completed", "Clear ICP defined"],
                "risks": ["Building before validation", "Too broad target audience"],
            },
            {
                "phase_title": "Phase 2 — MVP Definition",
                "objective": "Reduce the product to a sharp and testable first version.",
                "duration": "Week 3-4",
                "key_tasks": [
                    "Prioritize one core workflow",
                    "Define inputs, outputs, and user journey",
                    "Design simple system architecture",
                ],
                "deliverables": ["MVP scope", "Wireframes", "Architecture draft"],
                "success_metrics": ["Single core use case finalized", "Scope locked"],
                "risks": ["Feature creep", "Weak differentiation"],
            },
            {
                "phase_title": "Phase 3 — Build & Integrate",
                "objective": "Implement the first usable version with strong workflow reliability.",
                "duration": "Month 2",
                "key_tasks": [
                    "Build authentication and onboarding",
                    "Implement core AI workflow",
                    "Add logging and error handling",
                    "Create feedback capture loop",
                ],
                "deliverables": ["MVP build", "API layer", "User dashboard"],
                "success_metrics": ["Happy path works end to end", "First internal test completed"],
                "risks": ["Latency issues", "Prompt instability"],
            },
            {
                "phase_title": "Phase 4 — Launch & Learn",
                "objective": "Release to early users and improve using real usage signals.",
                "duration": "Month 3",
                "key_tasks": [
                    "Launch landing page",
                    "Onboard pilot users",
                    "Track activation and retention",
                    "Run weekly product review",
                ],
                "deliverables": ["Beta launch", "Feedback report", "Iteration plan"],
                "success_metrics": ["First paying or committed users", "Repeat usage trend"],
                "risks": ["Low adoption", "Messaging mismatch"],
            },
        ],
        "notes": [
            "Keep the first version narrow and measurable.",
            "Do not automate a workflow before validating that users care about it.",
            "Optimize for speed of learning before scale.",
        ],
    }

    system_prompt = """
You are a senior startup operator and AI product strategist.
Return only valid JSON matching this schema:
{
  "title": str,
  "summary": str,
  "readiness_score": int,
  "execution_mode": str,
  "tools_needed": list[str],
  "next_7_days": list[str],
  "next_30_days": list[str],
  "next_90_days": list[str],
  "phases": [
    {
      "phase_title": str,
      "objective": str,
      "duration": str,
      "key_tasks": list[str],
      "deliverables": list[str],
      "success_metrics": list[str],
      "risks": list[str]
    }
  ],
  "notes": list[str]
}
Make the roadmap realistic, concise, and execution-focused.
"""
    user_prompt = f"Planning context: {ctx}"
    draft = llm_service.generate_json(system_prompt, user_prompt, fallback)
    return {"draft_plan": draft}



def validator_node(state: RoadmapState) -> RoadmapState:
    draft = state["draft_plan"]
    notes = list(draft.get("notes", []))
    phases = draft.get("phases", [])

    if len(phases) < 4:
        notes.append("Roadmap was expanded to maintain launch realism.")

    score = max(35, min(int(draft.get("readiness_score", 60)), 92))
    draft["readiness_score"] = score
    draft["notes"] = list(dict.fromkeys(notes))
    draft["execution_mode"] = draft.get("execution_mode", "lean-mvp")
    return {"validated_plan": draft}



def formatter_node(state: RoadmapState) -> RoadmapState:
    validated = state["validated_plan"]
    response = RoadmapResponse(
        title=validated["title"],
        summary=validated["summary"],
        readiness_score=validated["readiness_score"],
        execution_mode=validated["execution_mode"],
        tools_needed=validated["tools_needed"],
        next_7_days=validated["next_7_days"],
        next_30_days=validated["next_30_days"],
        next_90_days=validated["next_90_days"],
        phases=[Phase(**phase) for phase in validated["phases"]],
        notes=validated.get("notes", []),
        raw_state={
            "normalized_goal": state.get("normalized_goal"),
            "planning_context": state.get("planning_context"),
        },
    )
    return {"final_output": response.model_dump()}



def build_graph():
    graph = StateGraph(RoadmapState)
    graph.add_node("intake", intake_node)
    graph.add_node("planner", planner_node)
    graph.add_node("validator", validator_node)
    graph.add_node("formatter", formatter_node)
    graph.add_edge(START, "intake")
    graph.add_edge("intake", "planner")
    graph.add_edge("planner", "validator")
    graph.add_edge("validator", "formatter")
    graph.add_edge("formatter", END)
    return graph.compile(checkpointer=checkpointer)


roadmap_graph = build_graph()



def run_roadmap_agent(payload: RoadmapRequest) -> RoadmapResponse:
    result = roadmap_graph.invoke(
        {"request": payload.model_dump()},
        config={"configurable": {"thread_id": f"roadmap::{payload.goal[:30]}::{payload.profile.name or 'guest'}"}},
    )
    return RoadmapResponse(**result["final_output"])
