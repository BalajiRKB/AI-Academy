from groq import Groq
from app.core.config import settings
from app.prompts.course_context import SYSTEM_PROMPT

client = Groq(api_key=settings.LLM_API_KEY)

async def get_llm_response(user_message: str) -> str:
    try:
        response = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=512,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"LLM error: {e}")
        return "Sorry, I'm having trouble answering right now. Please try again in a moment."
