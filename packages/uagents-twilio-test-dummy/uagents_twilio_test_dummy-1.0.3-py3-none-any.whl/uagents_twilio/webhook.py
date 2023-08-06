"""
This webhook file is just for sample to listen incoming message from twilio and pass it
to Agenet. Move it to your actual agent project and run it to listen messages.
"""
from typing import Annotated

from fastapi import FastAPI, Form
from models import WhatsAppWebhookMsg
from uagents.query import query

app = FastAPI()

AGENT_ADDRESS = "agent1qfrs3x9eh4pvaymsmwgjkjq4srqq4ctfw8h5hjduscmq4asq027tucn2gqw"


@app.post("/incoming")
async def incoming_message(Body: Annotated[str, Form()], From: Annotated[str, Form()]):
    # Extract relevant information from the incoming message
    print(Body, From)
    await query(
        destination=AGENT_ADDRESS,
        message=WhatsAppWebhookMsg(sender=From, msg=Body, start_message="Success"),
        timeout=10,
    )
