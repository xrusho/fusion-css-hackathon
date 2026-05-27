# Slack Outreach Relay API

Small backend service used by Oracle AI Studio via an External REST tool.

## What this does

* Receives a Slack outreach request from AI Studio
* Sends a direct message in Slack
* Returns a simple success/failure response
* Provides a health check for deployment verification

## Tech stack

* Python
* FastAPI
* Uvicorn
* Slack Web API

## Required environment variables

Create a `.env` file with:

```bash
SLACK_BOT_TOKEN=xoxb-your-slack-bot-token
API_KEY=hackathon-demo-key
```

## Install

```bash
pip install fastapi uvicorn slack_sdk python-dotenv
```

## Project structure

```text
app/
  main.py
.env
README.md
```

## API endpoints

### GET /health

Returns:

```json
{ "status": "ok" }
```

### POST /send-slack-outreach

Receives:

```json
{
  "recipient_slack_id": "U12345678",
  "message_text": "Hi Sarah, would you be open to a quick chat?"
}
```

Returns:

```json
{
  "status": "sent",
  "message_id": "slack-ts-value"
}
```

## Minimal FastAPI app

```python
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from slack_sdk import WebClient
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

if not SLACK_BOT_TOKEN:
    raise RuntimeError("Missing SLACK_BOT_TOKEN")
if not API_KEY:
    raise RuntimeError("Missing API_KEY")

slack_client = WebClient(token=SLACK_BOT_TOKEN)


class SlackPayload(BaseModel):
    recipient_slack_id: str
    message_text: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/send-slack-outreach")
def send_slack_outreach(
    payload: SlackPayload,
    x_api_key: str | None = Header(default=None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        response = slack_client.chat_postMessage(
            channel=payload.recipient_slack_id,
            text=payload.message_text
        )
        return {
            "status": "sent",
            "message_id": response.get("ts")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

## Run locally

```bash
uvicorn app.main:app --reload --port 8000
```

## Test locally

### Health check

```bash
curl http://localhost:8000/health
```

### Send outreach

```bash
curl -X POST http://localhost:8000/send-slack-outreach \
  -H "Content-Type: application/json" \
  -H "x-api-key: hackathon-demo-key" \
  -d '{
    "recipient_slack_id": "U12345678",
    "message_text": "Hi Sarah - you came up as a strong fit for a short-term internal task. Would you be open to a quick chat?"
  }'
```

## Deployment

Deploy this service to any public HTTPS host.

Examples:

* Render
* Railway
* Fly.io
* ngrok for local demo only

The deployed base URL is what Oracle AI Studio should use as the External REST tool instance URL.

## Oracle AI Studio configuration

Use:

* Instance URL: `https://your-backend-domain.com`
* Method: `POST`
* Path: `/send-slack-outreach`
* Header: `x-api-key: hackathon-demo-key`

Do not put Slack's API URL directly into AI Studio.

## Slack setup

1. Create a Slack app.
2. Add the `chat:write` scope.
3. Install the app to the workspace.
4. Copy the bot token.
5. Put the token in `SLACK_BOT_TOKEN`.

## Notes

* Keep the Slack token secret.
* AI Studio should send the outreach request to this backend.
* This backend sends the message to Slack.
