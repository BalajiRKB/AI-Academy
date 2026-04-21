from fastapi import FastAPI
from app.routes.webhook import router as webhook_router

app = FastAPI(title="AI Academy WhatsApp Chatbot", version="1.0.0")

app.include_router(webhook_router)

@app.get("/health")
def health():
    return {"status": "ok"}
