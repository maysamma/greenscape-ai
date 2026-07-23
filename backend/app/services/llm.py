import os
from typing import Any

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI


load_dotenv()


def get_llm() -> Any:
    provider = os.getenv(
        "LLM_PROVIDER",
        "gemini",
    ).strip().lower()

    if provider == "gemini":
        api_key = os.getenv("GOOGLE_API_KEY")
        model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash",
        )

        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY is missing. "
                "Add it to backend/.env"
            )

        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.2,
            google_api_key=api_key,
        )

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        model_name = os.getenv(
            "OPENAI_MODEL",
            "gpt-4o-mini",
        )

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is missing. "
                "Add it to backend/.env"
            )

        return ChatOpenAI(
            model=model_name,
            temperature=0.2,
            api_key=api_key,
        )

    raise ValueError(
        f"Unsupported LLM_PROVIDER: {provider}"
    )