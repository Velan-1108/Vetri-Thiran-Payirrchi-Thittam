from .gemini_client import gemini


def summarize_text(text: str) -> str:

    prompt = f"""
Summarize the following text for a student.

Text:
{text}

Rules:
- Give the main points.
- Include important information.
- Use simple and clear language.
- Keep the summary easy to understand.
"""

    return gemini.text(prompt)