from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from backend.core import CogniFlow
from fastapi.middleware.cors import CORSMiddleware
from backend.watcher import start_watcher
from contextlib import asynccontextmanager
import logging
import os
import time
import threading

logging.basicConfig(filename="./logs/logs", level=logging.INFO)

engine = CogniFlow()

def run_watcher_thread():
    observer = start_watcher("./documents/") 
    try:
        while True:
            time.sleep(1)
    except Exception as e:
        logging.error(f"Watcher background error: {e}")
    finally:
        observer.stop()
        observer.join()

@asynccontextmanager
async def lifespan(app: FastAPI):
    watcher_thread = threading.Thread(target=run_watcher_thread, daemon=True)
    watcher_thread.start()
    
    yield 

app = FastAPI(lifespan=lifespan)

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