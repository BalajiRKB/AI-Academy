import json
from fastapi import APIRouter, Request
from app.services.whapi_service import send_message
from app.services.llm_response import get_llm_response

router = APIRouter()

ENTRY_CODE = "AI-Academy"
WELCOME_MESSAGE = "Thank you for reaching out to the AI Academy! How can I help you today?"

@router.post("/webhook")
async def webhook(request: Request):
    try:
        body = await request.json()
        print("Webhook raw body:\n", json.dumps(body, indent=2))

        messages = body.get("messages", [])
        print(f"Webhook messages count: {len(messages)}")

        for message in messages:
            print("Webhook raw message:\n", json.dumps(message, indent=2))

            # For self-chat testing: allow from_me messages
            # In production with a different tester number, change this to:
            # if message.get("from_me"): continue
            msg_type = message.get("type")
            if msg_type != "text":
                print(f"Skipping non-text message type: {msg_type}")
                continue

            sender = message.get("chat_id") or message.get("from")
            text = message.get("text", {}).get("body", "").strip()

            print(f"Extracted sender: {sender}")
            print(f"Extracted text: {text}")

            if not sender or not text:
                print("Skipping: sender or text is empty")
                continue

            # Entry point check
            if text == ENTRY_CODE:
                print(f">>> Sending WELCOME message to {sender}")
                await send_message(sender, WELCOME_MESSAGE)
            else:
                print(f">>> Sending LLM response to {sender}")
                reply = await get_llm_response(text)
                await send_message(sender, reply)

    except Exception as e:
        print(f"Webhook error: {e}")

    return {"status": "ok"}
