# AI Academy WhatsApp Chatbot

A WhatsApp chatbot that answers student questions about the AI Academy course using an LLM. Built with **FastAPI**, **Whapi**, and **Groq (LLaMA 3.1)**.

---

## Features

- Entry point via `AI-Academy` trigger message
- Responds to course questions using LLM with fixed course context
- Handles modules, pricing, certificate, and enrollment queries
- Built-in fallback for out-of-scope questions
- Group message filtering to avoid noisy triggers

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| WhatsApp API | Whapi |
| LLM | Groq — LLaMA 3.1 8B Instant |
| Deployment | Local / Any server with public URL |

---

## Project Structure

```
AI-Academy/
├── app/
│   ├── main.py                   # FastAPI app entry point
│   ├── routes/
│   │   └── webhook.py            # Webhook handler
│   ├── services/
│   │   ├── llm_response.py       # Groq LLM integration
│   │   └── whapi_service.py      # Whapi message sending
│   ├── core/
│   │   └── config.py             # Environment config
│   └── prompts/
│       └── course_context.py     # System prompt + course context
├── LLD.md
├── README.md
├── requirements.txt
└── .env.example
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/BalajiRKB/AI-Academy.git
cd AI-Academy
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your values:

```env
WHAPI_TOKEN=your_whapi_token_here
WHAPI_BASE_URL=https://gate.whapi.cloud
LLM_API_KEY=your_groq_api_key_here
LLM_MODEL=llama-3.1-8b-instant
```

- Get your **Whapi token** from [whapi.cloud](https://whapi.cloud)
- Get your **Groq API key** from [console.groq.com](https://console.groq.com)

### 5. Run the server

```bash
uvicorn app.main:app --reload --port 8000
```

### 6. Expose with ngrok (for local testing)

```bash
ngrok http 8000
```

Copy the ngrok HTTPS URL and set it as your webhook in the Whapi dashboard:
```
https://your-ngrok-url.ngrok.io/webhook
```

---

## Testing the Bot

Send these messages from WhatsApp to your connected number:

| Message | Expected Response |
|---|---|
| `AI-Academy` | Welcome message |
| `What modules are available?` | Lists all 4 modules |
| `Is the course free?` | Free + ₹499 details |
| `How do I enroll?` | Payment page link |
| `Will I get a certificate?` | After all modules |
| `What's the weather?` | Polite out-of-scope redirect |

---

## Environment Variables

| Variable | Description |
|---|---|
| `WHAPI_TOKEN` | Your Whapi channel token |
| `WHAPI_BASE_URL` | Whapi API base URL |
| `LLM_API_KEY` | Groq API key |
| `LLM_MODEL` | LLM model name (e.g. `llama-3.1-8b-instant`) |

---

## Architecture

```
User (WhatsApp)
      ↓
   Whapi
      ↓ webhook
  FastAPI /webhook
      ↓
  Message Router
  ┌───────────┬─────────────────┐
  │ AI-Academy│  Course question│
  │  trigger  │                 │
  ↓           ↓
Welcome    Groq LLM
Message    (with course context)
      ↓           ↓
         Whapi send_message
              ↓
       User receives reply
```

---

## LLD

See [LLD.md](./LLD.md) for the full Low-Level Design including architecture, message flow, prompt design, and ban avoidance strategy.
