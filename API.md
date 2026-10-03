# API Documentation

The optional local FastAPI service is read-only and exposes analytics logged by the desktop application. Start it with `uvicorn revive_api:app --host 127.0.0.1 --port 8000`.

## `GET /health`
Returns service status.
```json
{"status":"ok","service":"hand-tracking-system"}
```

## `GET /api/v1/events?limit=100`
Returns up to 1,000 most recent SQLite events.
Response shape:
```json
{"count":1,"items":[{"id":1,"timestamp":"2026-10-03T12:00:00+00:00","event_type":"gesture_detected","gesture":"peace","finger_count":2,"fps":28.4,"details":""}]}
```

## `GET /api/v1/summary`
Returns aggregate counts from the latest 1,000 events.

## Interactive docs
FastAPI's OpenAPI UI is available at `/docs`; JSON schema is available at `/openapi.json`.

## Security
The service is intended for localhost/demo use. Do not expose it to the public internet without authentication, TLS, request limits, and a privacy/security review.
