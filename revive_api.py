"""Optional FastAPI read-only analytics API for the local event database."""
from fastapi import FastAPI, Query
from database import recent_events, init_db

app = FastAPI(title="Hand Tracking System API", version="1.0.0",
              description="Local analytics endpoints for the Hand Tracking System demo.")

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status":"ok","service":"hand-tracking-system"}

@app.get("/api/v1/events")
def events(limit: int = Query(default=100, ge=1, le=1000)):
    return {"count":len(recent_events(limit)), "items":recent_events(limit)}

@app.get("/api/v1/summary")
def summary():
    items=recent_events(1000)
    return {"events_total":len(items),
            "gestures_detected":sum(1 for x in items if x["event_type"]=="gesture_detected"),
            "screenshots":sum(1 for x in items if x["event_type"]=="screenshot"),
            "latest_event":items[0] if items else None}
