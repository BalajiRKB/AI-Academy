from fastapi import APIRouter, Request
from app.services.whapi_service import send_message
from app.services.llm_service import get_llm_response

router = APIRouter()

ENTRY_CODE = "AI-Academy"
WELCOME_MESSAGE = "Thank you for reaching out to the AI Academy! How can I help you today?"

@router.post("/webhook")
async def webhook(request: Request):
    try:
        body = await request.json()
        messages = body.get("messages", [])

        for message in messages:
            # Only handle incoming text messages
            if message.get("from_me"):
                continue

            msg_type = message.get("type")
            if msg_type != "text":
                continue

            sender = message.get("chat_id") or message.get("from")
            text = message.get("text", {}).get("body", "").strip()

            if not sender or not text:
                continue

            # Entry point check
            if text == ENTRY_CODE:
                await send_message(sender, WELCOME_MESSAGE)
            else:
                reply = await get_llm_response(text)
                await send_message(sender, reply)

    except Exception as e:
        print(f"Webhook error: {e}")

    return {"status": "ok"}
