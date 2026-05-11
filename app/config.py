"""
Loads configuration from environment variables / .env file.
Looks for .env in the project root (one level up from app/).
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Pin .env lookup to project root so it works no matter where streamlit is run from
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    FOUNDRY_ENDPOINT: str = os.getenv("FOUNDRY_ENDPOINT", "")
    FOUNDRY_API_KEY: str = os.getenv("FOUNDRY_API_KEY", "")
    MODEL_DEPLOYMENT_NAME: str = os.getenv("MODEL_DEPLOYMENT_NAME", "gpt-4o-mini")
    API_VERSION: str = os.getenv("API_VERSION", "2024-10-21")
    SYSTEM_PROMPT: str = os.getenv(
        "SYSTEM_PROMPT",
        "You are Asma, a helpful and professional AI agent. "
        "Answer the user's questions clearly, concisely, and with expertise."
    )

    def validate(self):
        missing = []
        if not self.FOUNDRY_ENDPOINT:
            missing.append("FOUNDRY_ENDPOINT")
        if not self.FOUNDRY_API_KEY:
            missing.append("FOUNDRY_API_KEY")
        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}. "
                f"Check your .env file at {env_path}."
            )


settings = Settings()
settings.validate()