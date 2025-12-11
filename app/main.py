from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from .controllers.chat_controller import ChatController
import uvicorn

import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

session_key = os.getenv("SESSION_SECRET_KEY")
if not session_key:
    raise RuntimeError("SESSION_SECRET_KEY missing from .env")

app.add_middleware(
    SessionMiddleware,
    secret_key=session_key
)

app.mount('/static', StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

chat_controller = ChatController()

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    chat_controller.ensure_user_session(request.session)
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/api/create_chat")
async def create_chat(request: Request):
    return chat_controller.create_chat(request.session)

@app.post("/api/send_message")
async def send_message(request: Request):
    data = await request.json()
    return chat_controller.send_message(request.session, data)