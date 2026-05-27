from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os
from pathlib import Path

print("Starting Slack test...")

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

token = os.getenv("SLACK_BOT_TOKEN")
print("Token loaded:", bool(token))

if not token:
    raise RuntimeError("SLACK_BOT_TOKEN is missing")

client = WebClient(token=token)

try:
    user_id = "U0B6EK07B5J"  # replace with your Slack member ID

    open_resp = client.conversations_open(users=user_id)
    print("conversations.open response:", open_resp)

    dm_channel_id = open_resp["channel"]["id"]

    msg_resp = client.chat_postMessage(
        channel=dm_channel_id,
        text="I would like your assistance regarding a finance initiative"
    )
    print("chat.postMessage response:", msg_resp)

except SlackApiError as e:
    print("Slack API error:", e.response["error"])
except Exception as e:
    print("Unexpected error:", repr(e))