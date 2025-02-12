import os
from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

from schemas.chat import Question
from service.rag import get_answer


load_dotenv()
OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")


app = FastAPI(
    title="AI Cocktail advisor",
)


templates = Jinja2Templates(directory="templates")


@app.get("/")
async def chat(request: Request):
    return templates.TemplateResponse(name="chat.html", context={"request": request})


@app.post("/chat/")
async def chat_post(question: Question):
    result = get_answer(question)
    return {"answer": f"{result}"}
