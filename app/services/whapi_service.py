import httpx
from app.core.config import settings

async def send_message(to: str, text: str) -> None:
    url = f"{settings.WHAPI_BASE_URL}/messages/text"
    headers = {
        "Authorization": f"Bearer {settings.WHAPI_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "to": to,
        "body": text,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        if response.status_code not in (200, 201):
            print(f"Whapi send failed: {response.status_code} {response.text}")
