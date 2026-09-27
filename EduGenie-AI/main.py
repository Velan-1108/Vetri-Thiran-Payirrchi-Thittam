from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from modules.gemini_client import gemini
from modules.quiz_module import QuizResult


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=30000)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=10000)


class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=10000)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
   return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={}
)

@app.post("/qa")
async def qa(payload: QuestionRequest):
    try:
        prompt = f"""
You are EduGenie, an educational learning assistant.

Answer the student's question clearly and accurately.

Student question:
{payload.question}

Give a simple explanation suitable for a student.
"""

        answer = gemini.text(prompt)

        return {"answer": answer}

    except Exception as exc:
        print("Q&A ERROR:", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/explain")
async def explain(payload: ExplainRequest):
    try:
        prompt = f"""
Explain the following topic in very simple language.

Topic:
{payload.topic}

Use:
- Simple words
- Short paragraphs
- Examples where useful
- Important points

Make it easy for a student to understand.
"""

        explanation = gemini.text(prompt)

        return {"answer": explanation}

    except Exception as exc:
        print("EXPLAIN ERROR:", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/quiz", response_model=QuizResult)
async def quiz(payload: TextRequest):
    try:
        prompt = f"""
Create a quiz for a student about:

{payload.text}

Rules:
- Create exactly 3 multiple-choice questions.
- Each question must have exactly 4 options.
- Provide the correct answer.
- Keep the questions educational and clear.
- The answer must exactly match one of the four options.
"""

        quiz_result = gemini.structured(prompt, QuizResult)

        return quiz_result

    except Exception as exc:
        print("QUIZ ERROR:", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/summarize")
async def summarize(payload: TextRequest):
    try:
        prompt = f"""
Summarize the following text for a student.

Text:
{payload.text}

Give:
- Main points
- Important information
- Simple and clear language
"""

        summary = gemini.text(prompt)

        return {"answer": summary}

    except Exception as exc:
        print("SUMMARY ERROR:", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/learn/recommendations")
async def learning_recommendations(payload: TextRequest):
    try:
        prompt = f"""
Create a beginner-to-advanced learning path for:

{payload.text}

Include:
1. Beginner topics
2. Intermediate topics
3. Advanced topics
4. Suggested timeline
5. Useful learning resources

Keep it clear and practical for a student.
"""

        recommendations = gemini.text(prompt)

        return {"answer": recommendations}

    except Exception as exc:
        print("LEARNING PATH ERROR:", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "message": "EduGenie backend is running"
    }