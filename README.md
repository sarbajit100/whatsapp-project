# WhatsApp Scheduler API

A FastAPI service that sends WhatsApp messages immediately or on a schedule using **Twilio**.

## Project structure

```
whatsapp-project/
├── app/
│   ├── __init__.py
│   ├── config.py       # Pydantic settings (reads .env)
│   ├── main.py         # FastAPI app + lifespan (scheduler start/stop)
│   ├── models.py       # Request / response schemas
│   ├── routes.py       # API endpoints
│   ├── scheduler.py    # APScheduler wrapper
│   └── whatsapp.py     # Twilio client
├── tests/
│   └── test_routes.py
├── main.py             # Entry point (python main.py)
├── requirements.txt
└── .env.example
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure credentials

```bash
cp .env.example .env
# Edit .env and fill in your Twilio credentials
```

| Variable | Description |
|---|---|
| `TWILIO_ACCOUNT_SID` | Your Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Your Twilio Auth Token |
| `TWILIO_WHATSAPP_FROM` | Sender number, e.g. `whatsapp:+14155238886` |

> **Sandbox:** Join the Twilio WhatsApp sandbox first — send `join <sandbox-word>` to `+14155238886` from your WhatsApp, then use `whatsapp:+14155238886` as the FROM number.

### 3. Run

```bash
python main.py
# or
uvicorn app.main:app --reload
```

API docs available at **http://localhost:8000/docs**

---

## Endpoints

### `POST /whatsapp/send`
Send a message immediately.

```json
{
  "to": "whatsapp:+919876543210",
  "message": "Hello from the API!"
}
```

### `POST /whatsapp/schedule`
Schedule a message for a future time.

```json
{
  "to": "whatsapp:+919876543210",
  "message": "Good morning!",
  "send_at": "2025-06-01T09:00:00+05:30"
}
```

Optionally add a **cron recurrence** (sends repeatedly):

```json
{
  "to": "whatsapp:+919876543210",
  "message": "Daily reminder",
  "send_at": "2025-06-01T09:00:00Z",
  "recurrence": "0 9 * * 1-5"
}
```

### `GET /whatsapp/jobs`
List all scheduled jobs.

### `GET /whatsapp/jobs/{job_id}`
Get status of a specific job (`pending` | `sent` | `failed` | `cancelled`).

### `DELETE /whatsapp/jobs/{job_id}`
Cancel a pending job.

### `GET /health`
Health check.

---

## Run tests

```bash
pytest tests/ -v
```
