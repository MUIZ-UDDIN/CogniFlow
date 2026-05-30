from fastapi import WebSocket
from core import CogniFlow

@app.WebSocket("/chat")

async def websocket_endpoint(websocket= WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()

        for words in CogniFlow.ask_question(data):
            await websocket.send_text(words)