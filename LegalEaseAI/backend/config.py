from functools import lru_cache
from pathlib import Path
import os

from dotenv import load_dotenv


ROOT_DIR = Path(__file__).resolve().parents[1]

load_dotenv(ROOT_DIR / ".env")


class Settings:

    app_name: str = os.getenv(
        "APP_NAME",
        "LegalEase"
    )

    gemini_api_key: str = os.getenv(
        "GEMINI_API_KEY",
        ""
    ).strip()

    gemini_model: str = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.8-flash"
    ).strip()

    backend_url: str = os.getenv(
        "BACKEND_URL",
        "http://127.0.0.1:8000"
    ).rstrip("/")

    max_document_chars: int = int(
        os.getenv(
            "MAX_DOCUMENT_CHARS",
            "50000"
        )
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()