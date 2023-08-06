from decouple import config
from uagents import Context, Protocol

from uagents_twilio.models import WhatsAppCustomMsg, WhatsAppWebhookMsg
from uagents_twilio.wrappers.smsWrapper import WhatsappClient

service_protocol = Protocol()

AGENT1_EMAIL = config("AGENT1_EMAIL")
AGENT2_EMAIL = config("AGENT2_EMAIL")

ACCOUNT_SID = config("ACCOUNT_SID")
AUTH_TOKEN = config("AUTH_TOKEN")
FROM_NUMBER = config("FROM_NUMBER")
TO_NUMBER = config("TO_NUMBER")


whatsapp_handler = WhatsappClient(
    agent=service_protocol,
    to_agent_address="agent1qfrs3x9eh4pvaymsmwgjkjq4srqq4ctfw8h5hjduscmq4asq027tucn2gqw",
    account_sid=ACCOUNT_SID,
    auth_token=AUTH_TOKEN,
    from_number=FROM_NUMBER,
    to_number=TO_NUMBER,
)


@service_protocol.on_query(model=WhatsAppWebhookMsg)
async def receive_msg(ctx: Context, sender: str, message: WhatsAppWebhookMsg):
    await ctx.send(sender, WhatsAppWebhookMsg(sender=message.sender, msg="Received"))
    ctx.storage.set("message", message.msg)
    whatsapp_handler.send_new_message(message.sender, message.start_message)


@service_protocol.on_message(model=WhatsAppCustomMsg)
async def send_wp_msg(ctx: Context, sender: str, message: WhatsAppCustomMsg):
    await ctx.send(
        sender,
        WhatsAppCustomMsg(receiver=message.receiver, msg="Sending a msg on Whatsapp"),
    )
    ctx.storage.set("message", message.msg)
    whatsapp_handler.send_new_message(message.receiver, message.msg)
