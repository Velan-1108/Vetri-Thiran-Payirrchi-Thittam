from .gemini_client import gemini


def explain_topic(topic: str) -> str:

    prompt = f"""
Explain the following topic to a student in very simple language.

Topic:
{topic}

Rules:
- Use simple words.
- Explain the basic idea first.
- Give a simple example.
- Mention important points.
- Keep it clear and easy to understand.
"""

    return gemini.text(prompt)