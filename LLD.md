# LLD - AI Academy WhatsApp Chatbot

## 1. Overview

For this assignment, I am building a WhatsApp chatbot for the AI Academy course using **FastAPI** as the backend, **Whapi** as the WhatsApp API layer, and an **LLM** for generating responses. The main goal of the bot is to answer student questions about the AI Academy course, provide pricing and module information, and guide users towards enrollment using the given payment link.  

This chatbot is intentionally kept simple and focused because the task does not require a full product, dashboard, or retrieval pipeline. The assignment explicitly mentions that **RAG is not needed**, and that the course details can be passed directly into the LLM context window.  

---

## 2. Objective

The objective of this chatbot is to:

- Understand user queries related to the AI Academy course.  
- Respond using LLM-based responses.  
- Provide course-related information such as modules, pricing, and certification.  
- Guide the user to enrollment using the payment page link.  

---

## 3. Scope

This chatbot supports only AI Academy course-related conversations. It is not designed to answer general questions outside the provided course context. The chatbot starts the conversation only when the user sends the code **`AI-Academy`**.  

The bot will then respond with the exact required message:

**"Thank you for reaching out to the AI Academy! How can I help you today?"**  

---

## 4. Functional Requirements

The chatbot should support the following:

1. Receive incoming WhatsApp messages from users through Whapi.  
2. Detect whether the user has sent the entry code `AI-Academy`.  
3. Send the predefined welcome response when the entry code is received.  
4. Accept follow-up questions related to the AI Academy course.  
5. Use an LLM to generate responses based on the provided course information.  
6. Answer questions related to:
   - Course modules  
   - Learning units in each module  
   - Free vs paid access  
   - Course pricing  
   - Certificate availability  
   - Enrollment guidance using the payment page  
7. Send the generated response back to the user on WhatsApp through Whapi.  

---

## 5. Non-Functional Requirements

1. The bot should provide quick responses for a smooth chat experience.
2. The architecture should be simple and easy to understand during the code walkthrough.
3. The implementation should be safe for limited testing and should reduce the risk of WhatsApp number bans.  
4. The project structure should be clean enough to be reviewed easily through GitHub.  

---

## 6. Course Context Used by the LLM

The LLM will receive the following course details as fixed context:  

- Module 1: Introduction to LLM — 10 Learning Units  
- Module 2: Basics of Prompting — 12 Learning Units  
- Module 3: Deep Dive into LLM Integration — 15 Learning Units  
- Module 4: Advanced LLM Concepts and Agentic AI — 17 Learning Units  

Access and pricing details:  

- Module 1 and Module 2 are free.  
- Module 3 and Module 4 require payment of ₹499.  
- Payment page: `https://ai-academy.example.com/pricing`  
- After completing all modules, users can download a completion certificate.  

Since the task clearly states that **RAG-based retrieval is not needed**, I am directly passing this course information into the LLM context window.  

---

## 7. High-Level Architecture

The chatbot system consists of the following components:

### 7.1 User
The student interacts with the chatbot through WhatsApp.

### 7.2 Whapi
Whapi is used as the WhatsApp API service for receiving incoming messages and sending bot replies. The task specifically requires Whapi to be used for the chatbot API layer.  

### 7.3 FastAPI Backend
The FastAPI backend acts as the core application layer. It receives webhook events from Whapi, processes the incoming message, decides how to handle it, calls the LLM if needed, and sends the final reply back through Whapi.

### 7.4 LLM Service
The LLM is responsible for generating natural language responses based only on the provided AI Academy course context. The project uses **Groq (LLaMA 3.1 8B Instant)** as the LLM provider.

---

## 8. Architecture Flow

The complete flow is:

1. User sends a WhatsApp message.
2. Whapi receives the message and triggers the configured webhook.
3. FastAPI receives the webhook event.
4. The backend extracts the sender number and message text.
5. Group messages and non-text messages are filtered out.
6. If the message is `AI-Academy`, the backend sends the predefined welcome message.  
7. If the message is a course-related question, the backend sends:
   - System prompt
   - Fixed AI Academy course context
   - User message  
   to the LLM.  
8. The LLM generates a context-aware response.
9. FastAPI sends this response back to the user through Whapi.
10. The user receives the reply on WhatsApp.

---

## 9. Message Handling Logic

### 9.1 Entry Point Logic
If the user message exactly matches `AI-Academy`, the bot sends:

**"Thank you for reaching out to the AI Academy! How can I help you today?"**  

### 9.2 Course Query Logic
If the user asks a question related to modules, pricing, certification, or enrollment, the backend forwards the question to the LLM along with the fixed course context.  

### 9.3 Out-of-Scope Logic
If the user asks something unrelated to AI Academy, the bot will respond politely and redirect the conversation back to supported topics such as modules, pricing, certificate, or enrollment.

Example fallback:
> I can help you with AI Academy course details like modules, pricing, certificate, and enrollment.

### 9.4 Group Message Filter
Messages from WhatsApp group chats (identified by `@g.us` in the chat ID) are automatically skipped to prevent the bot from responding in groups.

---

## 10. API Design

### 10.1 Health Check Endpoint
**GET /health**

Purpose:
- Used to verify that the FastAPI backend is running properly.

Response:
```json
{
  "status": "ok"
}
```

### 10.2 Webhook Endpoint
**POST /webhook**

Purpose:
- Receives incoming WhatsApp events from Whapi.
- Extracts user message details.
- Processes chatbot logic.
- Sends reply through Whapi.

Expected responsibilities:
- Parse webhook payload
- Validate incoming message
- Filter group messages and non-text types
- Detect entry message
- Route normal queries to LLM
- Return success response to Whapi

---

## 11. Prompt Design

The chatbot uses a fixed system prompt to make the model behave like a course assistant.

### System Prompt Intent
The prompt will instruct the LLM to:

- Act as the AI Academy WhatsApp assistant.
- Answer only from the provided course information.  
- Avoid making up facts outside the provided context.
- Guide users to the pricing page when they ask about enrollment.  
- Keep responses short, clear, and student-friendly.

### Why this prompt design
This approach is enough for the assignment because the task only requires dynamic answers from the given context and explicitly says RAG is unnecessary.  

---

## 12. Internal Modules

### 12.1 Webhook Handler
Responsible for receiving and parsing incoming WhatsApp events.

### 12.2 Message Processor
Responsible for:
- Identifying whether the message is the entry code
- Filtering group messages and non-text types
- Deciding whether to send the fixed welcome reply or call the LLM
- Handling unsupported or empty messages

### 12.3 LLM Response Service (`llm_response.py`)
Responsible for:
- Building the prompt
- Attaching course context
- Sending the request to Groq LLM
- Returning the generated text response

### 12.4 Whapi Service
Responsible for:
- Sending outbound WhatsApp replies
- Handling API token authentication
- Calling the Whapi send message endpoint

### 12.5 Config Module
Responsible for:
- Loading environment variables
- Storing API keys and tokens securely
- Separating configuration from code

---

## 13. Project Structure

```bash
AI-Academy/
│
├── app/
│   ├── main.py
│   ├── routes/
│   │   └── webhook.py
│   ├── services/
│   │   ├── llm_response.py
│   │   └── whapi_service.py
│   ├── core/
│   │   └── config.py
│   └── prompts/
│       └── course_context.py
│
├── README.md
├── LLD.md
├── requirements.txt
└── .env.example
```

This structure is intentionally simple because the assignment is focused on chatbot flow and clarity rather than scale.  

---

## 14. Error Handling

The chatbot should handle basic errors gracefully:

1. If the incoming payload is invalid, the webhook should return a safe error response.
2. If the LLM call fails, the bot should return a polite fallback message such as:
   > Sorry, I'm having trouble answering right now. Please try again in a moment.
3. If Whapi sending fails, the error should be logged for debugging.
4. If the message is empty or unsupported, the bot should avoid unnecessary replies.

This is enough for the current assignment scope.

---

## 15. Ban Avoidance Strategy

This section is important because the task explicitly asks for information on how the chatbot avoids the WhatsApp number from getting banned.  

To reduce the risk of bans, I will follow these practices:

1. **Single known number testing**  
   I will test the bot only using one known personal number, because the assignment clearly warns that sending messages to multiple numbers using third-party APIs may result in the WhatsApp number being blocked.  

2. **No bulk messaging**  
   The chatbot will not send messages proactively to random users. It will only reply when a user sends a message first.

3. **No spam-like behavior**  
   The backend will not send repeated automated messages, loops, or unnecessary retries.

4. **Inbound-only interaction model**  
   The bot will work as a reply-based chatbot, not as a campaign or broadcast system. This makes the usage pattern safer.

5. **Group message filtering**  
   The bot automatically skips all messages from WhatsApp groups (`@g.us`), preventing unintended replies in group chats which can trigger spam detection.

6. **Low-volume testing**  
   Since this is only an assignment demo, the usage volume will remain very low during development and testing.  

7. **No multi-user rollout during assignment**  
   I will not distribute the bot publicly or test it with many different numbers during this task round.

These practices align with the warning mentioned in the task document and help keep testing controlled and safe.  

---

## 16. Why FastAPI Was Chosen

I chose FastAPI because this assignment mainly needs a webhook-based backend that can receive events, process requests, and send API calls efficiently. FastAPI is lightweight, easy to structure, and a good fit for building a clean chatbot backend for a small but complete assignment.

It also makes the project easier to explain during the architecture walkthrough because the request flow remains straightforward:
**Whapi → FastAPI → LLM → Whapi**.

---

## 17. Example User Questions Supported

The chatbot should be able to answer questions such as:

- What modules are included in the AI Academy course?  
- Is the course free or paid?  
- What is taught in Module 3?  
- How much does the full course cost?  
- Will I get a certificate after completing the course?  
- How can I enroll in the paid modules?  

These examples are directly aligned with the course context provided in the task.  

---

## 18. Final Notes

This design keeps the chatbot simple, assignment-focused, and easy to demonstrate. It covers the required WhatsApp integration, LLM-based response generation, course information support, enrollment guidance, and number-ban prevention strategy without adding unnecessary complexity like RAG or large-scale infrastructure.  

The implementation is designed to match the task requirements exactly and to be easy to explain in the GitHub repository and video walkthrough.  
