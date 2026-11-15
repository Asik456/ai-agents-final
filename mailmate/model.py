import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def make_model():
    key = os.getenv("LLM_API_KEY")
    if not key:
        raise RuntimeError("LLM_API_KEY is missing. Copy .env.example to .env and add your key.")
    return ChatOpenAI(
        model=os.getenv("LLM_MODEL", "openai/gpt-5.6-luna"),
        api_key=key,
        base_url=os.getenv("LLM_BASE_URL", "https://openrouter.ai/api/v1"),
        use_responses_api=False,
        timeout=30,
        max_retries=2,
    )
