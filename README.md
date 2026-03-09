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

## Future Improvements

- Add authentication and role-based access controls
- Add retry and dead-letter handling for failed events
- Add unit tests and basic CI pipeline
