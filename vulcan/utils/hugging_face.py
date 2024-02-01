import requests

from vulcan.configs.llm import LLM


def llm_api(payload, can_retry=True):
    try:
        response = requests.post(
            LLM.HuggingFace.API_URL,
            headers=LLM.HuggingFace.API_HEADERS,
            json=payload,
        )
        return response.json()[0]["generated_text"]
    except KeyError:
        if can_retry:
            return llm_api(payload, False)
        return response.json()
