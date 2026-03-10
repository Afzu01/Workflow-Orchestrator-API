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
uvicorn app.main:app --reload --port 8001
```

Open after startup (local machine only): [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

## For Recruiters

- Local API docs: http://127.0.0.1:8001/docs
- Live deployment URL: add after deployment
- Suggested screenshots:
	- docs_home.png
	- event_create_response.png

Sample request
POST /events
{
	"source": "n8n",
	"event_type": "order.created"
}

Sample response
{
	"id": 1,
	"source": "n8n",
	"event_type": "order.created",
	"status": "queued"
}

## Future Improvements

- Add authentication and role-based access controls
- Add retry and dead-letter handling for failed events
- Add unit tests and basic CI pipeline
