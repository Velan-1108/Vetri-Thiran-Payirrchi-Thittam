from pydantic import BaseModel, Field

from .gemini_client import gemini


class QuizQuestion(BaseModel):
    question: str
    options: list[str] = Field(
        min_length=4,
        max_length=4
    )
    answer: str


class QuizResult(BaseModel):
    questions: list[QuizQuestion] = Field(
        min_length=3,
        max_length=3
    )


def generate_quiz(topic: str) -> QuizResult:

    prompt = f"""
Create a quiz for a student about:

{topic}

Rules:
- Create exactly 3 multiple-choice questions.
- Each question must have exactly 4 options.
- Provide the correct answer.
- The answer must exactly match one of the 4 options.
- Keep the questions educational and clear.
"""

    return gemini.structured(
        prompt,
        QuizResult
    )