# RoadPilot AI

**RoadPilot AI** is a premium roadmap-generation SaaS scaffold with a futuristic **Neural Command UI** and a LangGraph-based workflow engine.

**Created by Raja Abimanyu N — Data Scientist | AI & Applied Machine Learning**

## What this build includes

- LangGraph workflow orchestration
- FastAPI backend
- React + Vite frontend
- Profile-aware roadmap generation
- Readiness scoring
- 7 / 30 / 90 day execution planning
- Neural Command glassmorphism UI
- Creator branding built into the product footer and API metadata

## Workflow

```text
User Goal
   ↓
Intake Node
   ↓
Planner Node
   ↓
Validator Node
   ↓
Formatter Node
   ↓
Final Roadmap Output
```

LangGraph is designed around shared state, nodes, and edges, and its official docs highlight persistence, durable execution, streaming, and human-in-the-loop as core production capabilities. When a graph is compiled with a checkpointer, state is persisted in threads/checkpoints and can be resumed later. citeturn640608search2turn640608search4turn640608search6

## Project structure

```text
roadpilot_ai_fullstack/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── graphs/
│   │   ├── models/
│   │   └── services/
│   ├── tests/
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── lib/
│   │   └── styles/
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## Backend setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate   # macOS / Linux
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Frontend setup

```bash
cd frontend
npm install
npm run dev
```

## Example request

```json
{
  "goal": "I want to build an AI SaaS for recruiters.",
  "goal_type": "ai_saas",
  "profile": {
    "name": "Raja",
    "experience_level": "intermediate",
    "technical_background": true,
    "budget_range": "medium",
    "timeline_months": 6,
    "country": "India",
    "market": "Recruitment Tech",
    "team_size": "solo",
    "current_skills": ["Python", "FastAPI", "LLMs"],
    "constraints": ["Part-time founder", "Lean budget"]
  }
}
```

## Suggested next upgrades

- Postgres checkpointer for persistent threads
- user authentication
- PDF export
- Stripe billing
- saved roadmap history
- analytics and tracing
- richer goal templates
- human approval interruptions for sensitive actions

LangGraph’s official docs explicitly note that compiling with a checkpointer enables persistence and durable execution, and interrupt-based pauses support human-in-the-loop workflows that can be resumed by thread ID. citeturn640608search0turn640608search1turn640608search4
