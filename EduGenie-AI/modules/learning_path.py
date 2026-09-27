from .gemini_client import gemini


def get_learning_recommendations(topic: str) -> str:

    prompt = f"""
Create a beginner-to-advanced learning path for:

{topic}

Include:

1. Beginner topics
2. Intermediate topics
3. Advanced topics
4. Suggested timeline
5. Useful learning resources

Rules:
- Keep it practical for a student.
- Use simple language.
- Organize the learning path clearly.
"""

    return gemini.text(prompt)