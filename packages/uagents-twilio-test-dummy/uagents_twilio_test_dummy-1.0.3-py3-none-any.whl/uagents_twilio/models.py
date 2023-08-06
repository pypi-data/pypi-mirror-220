# Start writing uagents models from here
from uagents import Model


class WhatsAppWebhookMsg(Model):
    sender: str
    msg: str
    start_message: str


class WhatsAppCustomMsg(Model):
    receiver: str
    msg: str
