from google import genai
from app.core.config import settings
from app.prompts.course_context import SYSTEM_PROMPT

client = genai.Client(api_key=settings.LLM_API_KEY)

async def get_llm_response(user_message: str) -> str:
    try:
        response = client.models.generate_content(
            model=settings.LLM_MODEL,
            contents=user_message,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "max_output_tokens": 512,
            }
        )
        return response.text
    except Exception as e:
        print(f"LLM error: {e}")
        return "Sorry, I'm having trouble answering right now. Please try again in a moment."
