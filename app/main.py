import os

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from slack_sdk import WebClient

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


@app.get("/")
def root():
    return {"status": "ok", "message": "Slack relay is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/send-slack-outreach")
def send_slack_outreach(
    payload: SlackPayload,
    x_api_key: str | None = Header(default=None),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        response = slack_client.chat_postMessage(
            channel=payload.recipient_slack_id,
            text=payload.message_text,
        )
        return {
            "status": "sent",
            "message_id": response.get("ts"),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
