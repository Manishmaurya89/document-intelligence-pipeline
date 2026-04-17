import time
import requests
from config import OLLAMA_URL, DEFAULT_MODEL


def build_prompt(topic, pages):
    words = pages * 400  # ~400 words per page

    return f"""
Write a detailed article on "{topic}".

Requirements:
- Length: {words} words
- Include:
  - Title
  - Introduction
  - 5-7 sections with headings
  - Conclusion
- Each section should be detailed (6-8 lines)
- Add a table ONLY if relevant

Rules:
- No markdown (**)
- No repetition
- Keep content informative and structured
"""


def generate_document(topic, pages, retries=3):
    prompt = build_prompt(topic, pages)

    for attempt in range(retries):
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": DEFAULT_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": pages * 500
                    }
                },
                timeout=120
            )

            data = response.json()

            if "response" not in data:
                raise ValueError(f"Ollama error: {data}")

            text = data["response"]

            lines = [
                line.strip().replace("**", "")
                for line in text.split("\n")
                if line.strip()
            ]

            return lines

        except Exception as e:
            print(f"[Attempt {attempt + 1}/{retries}] Generation failed: {e}")
            if attempt < retries - 1:
                time.sleep(3)

    raise RuntimeError("Document generation failed after all retries.")
