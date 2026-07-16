"""
Thin wrapper around the Groq API so agents don't repeat boilerplate.
Uses Llama 3.3 70B via Groq for fast, cheap reasoning.
"""
import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
def ask_llm(system_prompt: str, user_prompt: str, json_mode: bool = False, temperature: float = 0.2):
    """
    Single call helper. If json_mode=True, asks the model to return
    strictly valid JSON and parses it before returning.
    """
    if _client is None:
        raise RuntimeError(
            "GROQ_API_KEY not set. Add it to backend/.env (see .env.example)."
        )

    kwargs = {}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    completion = _client.chat.completions.create(
        model=MODEL,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        **kwargs,
    )

    text = completion.choices[0].message.content

    if json_mode:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Model occasionally wraps JSON in markdown fences - strip and retry
            cleaned = text.strip().strip("`").replace("json\n", "", 1)
            return json.loads(cleaned)

    return text
