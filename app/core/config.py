from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    WHAPI_TOKEN: str
    WHAPI_BASE_URL: str = "https://gate.whapi.cloud"
    LLM_API_KEY: str
    LLM_MODEL: str = "llama-3.1-8b-instant"

    class Config:
        env_file = ".env"

settings = Settings()
