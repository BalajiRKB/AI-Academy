import google.generativeai as genai
from app.core.config import settings
from app.prompts.course_context import SYSTEM_PROMPT

genai.configure(api_key=settings.LLM_API_KEY)

async def get_llm_response(user_message: str) -> str:
    try:
        model = genai.GenerativeModel(
            model_name=settings.LLM_MODEL,
            system_instruction=SYSTEM_PROMPT
        )
        response = model.generate_content(user_message)
        return response.text
    except Exception as e:
        print(f"LLM error: {e}")
        return "Sorry, I'm having trouble answering right now. Please try again in a moment."
