from decouple import config
from uagents import Context, Protocol

from uagents_twilio.models import WhatsAppMsg
from uagents_twilio.wrappers.messageWrapper import WhatsappClient

service_protocol = Protocol()

AGENT1_EMAIL = config("AGENT1_EMAIL")
AGENT2_EMAIL = config("AGENT2_EMAIL")

# gc = GoogleCalendar(
#     calendar=AGENT1_EMAIL,
#     authentication_flow_port=8080,
#     token_path=token_path,
# )

# calendar_handler = GCAgentHandler(
#     agent=service_protocol,
#     agent_email=AGENT1_EMAIL,
#     gc=gc,
#     events_mapping={},
# )


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


@service_protocol.on_query(model=WhatsAppMsg)
async def receive_msg(ctx: Context, sender: str, message: WhatsAppMsg):
    await ctx.send(sender, WhatsAppMsg(sender=message.sender, msg="Received"))
    ctx.storage.set("message", message.msg)
    whatsapp_handler.send_new_message(message.sender, "Success .")
    # if "fetch" in message.msg:
    #     print(message.msg)
    #     event = ctx.storage.get("event")
    #     event_data = calendar_handler.event_dict(event)
    #     summary = event["summary"]
    #     message.msg = summary
    #     print(message.msg)
    #     whatsapp_handler.send_new_message(message.sender, f"This is your upcoming event:\n {event_data}\nBy selecting the yes/no option, let me know if you want me to carry out this task.")
    # elif message.msg == "yes":
    #     event = ctx.storage.get("event")
    #     summary = event["summary"]
    #     message.msg = summary
    # elif message.msg == "no":
    #     whatsapp_handler.send_new_message(message.sender, f"How else may I help you?")
