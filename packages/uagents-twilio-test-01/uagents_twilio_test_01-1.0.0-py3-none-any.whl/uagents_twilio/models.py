# Start writing pydantic models from here
from uagents import Model


class WhatsAppMsg(Model):
    sender: str
    msg: str
