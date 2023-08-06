from typing import Annotated

from fastapi import FastAPI, Form
from models import WhatsAppMsg
from uagents.query import query

app = FastAPI()

AGENT_ADDRESS = "agent1qfrs3x9eh4pvaymsmwgjkjq4srqq4ctfw8h5hjduscmq4asq027tucn2gqw"


@app.post("/incoming")
async def incoming_message(Body: Annotated[str, Form()], From: Annotated[str, Form()]):
    # Extract relevant information from the incoming message
    print(Body, From)
    await query(
        destination=AGENT_ADDRESS,
        message=WhatsAppMsg(sender=From, msg=Body),
        timeout=10,
    )
