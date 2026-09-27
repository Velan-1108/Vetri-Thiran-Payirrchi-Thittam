from .gemini_client import gemini


def answer_question(question: str) -> str:

    prompt = f"""
You are EduGenie, an educational AI tutor.

Answer the student's question clearly and accurately.

Student question:
{question}

Rules:
- Use simple language.
- Explain step by step when useful.
- Give examples when helpful.
- Do not make the answer unnecessarily complicated.
"""

    return gemini.text(prompt)