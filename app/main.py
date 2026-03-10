from datetime import datetime
from enum import Enum
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sqlalchemy import DateTime, Enum as SAEnum, Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Status(str, Enum):
    queued = "queued"
    processed = "processed"
    failed = "failed"


class Base(DeclarativeBase):
    pass


class WorkflowEvent(Base):
    __tablename__ = "workflow_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(100))
    event_type: Mapped[str] = mapped_column(String(100))
    status: Mapped[Status] = mapped_column(SAEnum(Status), default=Status.queued)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class EventCreate(BaseModel):
    source: str = Field(..., min_length=2)
    event_type: str = Field(..., min_length=2)


class EventUpdate(BaseModel):
    status: Status


engine = create_engine("sqlite:///data/events.db", echo=False)
Base.metadata.create_all(engine)

app = FastAPI(title="Workflow Orchestrator API", version="1.0.0")
UI_FILE = Path(__file__).resolve().parent.parent / "ui" / "index.html"


@app.get("/")
def root() -> dict:
    return {"message": "Workflow Orchestrator API", "docs": "/docs", "ui": "/ui"}


@app.get("/ui")
def ui() -> FileResponse:
    return FileResponse(UI_FILE)


@app.post("/events")
def create_event(payload: EventCreate) -> dict:
    with Session(engine) as session:
        event = WorkflowEvent(source=payload.source, event_type=payload.event_type)
        session.add(event)
        session.commit()
        session.refresh(event)
        return {
            "id": event.id,
            "source": event.source,
            "event_type": event.event_type,
            "status": event.status,
            "created_at": event.created_at.isoformat(),
        }


@app.get("/events")
def list_events() -> list[dict]:
    with Session(engine) as session:
        events = session.query(WorkflowEvent).order_by(WorkflowEvent.id.desc()).all()
        return [
            {
                "id": e.id,
                "source": e.source,
                "event_type": e.event_type,
                "status": e.status,
                "created_at": e.created_at.isoformat(),
            }
            for e in events
        ]


@app.patch("/events/{event_id}")
def update_event(event_id: int, payload: EventUpdate) -> dict:
    with Session(engine) as session:
        event = session.get(WorkflowEvent, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        event.status = payload.status
        session.commit()
        session.refresh(event)
        return {"id": event.id, "status": event.status}
