ROADMAP_BLUEPRINTS = {
    "ai_saas": {
        "focus": [
            "problem validation",
            "customer interviews",
            "MVP scope definition",
            "LLM stack and infra planning",
            "pricing and go-to-market",
            "launch and iteration",
        ],
        "tools": ["FastAPI", "React", "Postgres", "OpenAI API", "Stripe", "Vercel/Render"],
    },
    "ai_business": {
        "focus": [
            "offer design",
            "service packaging",
            "proof of value",
            "lead generation",
            "operations and delivery",
        ],
        "tools": ["Notion", "Calendly", "CRM", "OpenAI API", "LinkedIn"],
    },
    "general": {
        "focus": [
            "clarify objective",
            "assess current readiness",
            "map execution phases",
            "set milestones",
            "track outcomes",
        ],
        "tools": ["Docs", "Task tracker", "Spreadsheet", "LLM assistant"],
    },
}


def select_blueprint(goal_type: str) -> dict:
    return ROADMAP_BLUEPRINTS.get(goal_type, ROADMAP_BLUEPRINTS["general"])
