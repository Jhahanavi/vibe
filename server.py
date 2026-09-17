from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn
import json
from datetime import datetime

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "online",
        "service": "SoundVibe Streaming Server"
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    print("Raspberry Pi connected.")

    try:
        while True:
            data = await websocket.receive_text()

            try:
                vibration = json.loads(data)

                print(
                    f"Received | "
                    f"X: {vibration.get('x_g')} g | "
                    f"Y: {vibration.get('y_g')} g | "
                    f"Z: {vibration.get('z_g')} g"
                )

                # Send acknowledgement back to Raspberry Pi
                await websocket.send_text(
                    json.dumps({
                        "status": "received",
                        "timestamp": datetime.utcnow().isoformat()
                    })
                )

            except json.JSONDecodeError:
                print("Invalid JSON received.")

    except WebSocketDisconnect:
        print("Raspberry Pi disconnected.")

    except Exception as e:
        print(f"Connection error: {e}")


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000
    )
