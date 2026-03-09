# Workflow Orchestrator API

I built this backend project to demonstrate webhook-style event ingestion and workflow status tracking with clean API design.

## Features

- Create workflow events through REST APIs
- Track event status lifecycle (`queued`, `processed`, `failed`)
- Persist event data in SQLite
- Keep the project structure simple and easy to extend

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open: http://127.0.0.1:8000/docs

## Why this project helps internship applications

- Shows end-to-end backend ownership
- Demonstrates schema design, persistence, and API contracts
- Aligns with webhook and workflow responsibilities
