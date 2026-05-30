from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from backend.core import CogniFlow
import logging

logging.basicConfig(filename="./logs/logs", level=logging.INFO)

engine = CogniFlow()

app = FastAPI()

@app.websocket("/chat")

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()

            for words in engine.ask_question(data):
                await websocket.send_text(words)
    
    except WebSocketDisconnect:
        logging.info("User has disconnected gracefully!")