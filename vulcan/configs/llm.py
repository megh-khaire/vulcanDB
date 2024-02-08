import os


class LLM:
    class HuggingFace:
        API_URL = os.getenv("HF_API_URL")
        API_TOKEN = os.getenv("HF_API_TOKEN")
        API_HEADERS = {"Authorization": f"Bearer {API_TOKEN}"}

    class OpenAI:
        MODEL = "gpt-3.5-turbo"
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
