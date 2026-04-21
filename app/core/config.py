from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    WHAPI_TOKEN: str
    WHAPI_BASE_URL: str = "https://gate.whapi.cloud"
    LLM_API_KEY: str
    LLM_MODEL: str = "gemini-2.0-flash"

    class Config:
        env_file = ".env"

settings = Settings()
