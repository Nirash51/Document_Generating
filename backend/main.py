from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import get_settings
from backend.routes import router


settings = get_settings()


app = FastAPI(

    title=settings.app_name,

    version="1.0.0",

    description=(
        "AI-assisted legal "
        "document drafting API."
    ),
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"],
)


app.include_router(router)


@app.get(
    "/",
    tags=["System"]
)
def root():

    return {

        "app":
            settings.app_name,

        "status":
            "running",

        "docs":
            "/docs",

        "health":
            "/health",
    }


@app.get(
    "/health",
    tags=["System"]
)
def health():

    return {

        "status":
            "ok",

        "gemini_configured":
            bool(
                settings.gemini_api_key
            ),

        "model":
            settings.gemini_model,
    }