import os
from dotenv import load_dotenv


load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

USE_LOCAL_EXPLAINER = os.getenv(
    "USE_LOCAL_EXPLAINER",
    "false"
).lower() == "true"

USE_MOCK_AI = os.getenv(
    "USE_MOCK_AI",
    "false"
).lower() == "true"