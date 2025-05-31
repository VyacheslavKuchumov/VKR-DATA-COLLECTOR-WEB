from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.websocketController import process_message
from app.websocket.connectionManager import manager

router = APIRouter()

@router.websocket("/ws/{job_id}")
async def websocket_endpoint(websocket: WebSocket, job_id: str):
    """
    Clients connect to /ws/{job_id} to both send control messages
    (if you support them) and receive broadcasts for that job.
    """
    # 1) accept & register under this job_id
    await manager.connect(job_id, websocket)

    try:
        while True:
            # (optional) receive from client
            data = await websocket.receive_text()
            # let your controller do something if needed
            response = await process_message(data)

            # 2) broadcast to everyone listening on this job_id
            await manager.broadcast(job_id, response)

    except WebSocketDisconnect:
        # 3) clean up
        manager.disconnect(job_id, websocket)
        print(f"Client disconnected from job {job_id}")
