from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from backend.core import CogniFlow
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

logging.basicConfig(filename="./logs/logs", level=logging.INFO)

engine = CogniFlow()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/chat")

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            UserQuestion = data["question"]
            SelectedDoc = data["file"]

            for words in engine.ask_question(UserQuestion, SelectedDoc):
                await websocket.send_text(words)

    except WebSocketDisconnect:
        logging.info("User has disconnected gracefully!")

@app.get("/files")  

async def files():
    dir_path = "./documents"

    if not os.path.exists(dir_path):
        return []

    pdf_files = [f for f in os.listdir(dir_path) if f.endswith(".pdf")]

    return pdf_files