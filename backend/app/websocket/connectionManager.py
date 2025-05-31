from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.jobs: dict[str, set[WebSocket]] = {}

    async def connect(self, job_id: str, ws: WebSocket):
        await ws.accept()
        self.jobs.setdefault(job_id, set()).add(ws)

    def disconnect(self, job_id: str, ws: WebSocket):
        self.jobs.get(job_id, set()).discard(ws)

    async def broadcast(self, job_id: str, message: str):
        for ws in list(self.jobs.get(job_id, [])):
            try:
                await ws.send_text(message)
            except:
                self.disconnect(job_id, ws)


# Instantiate the connection manager
manager = ConnectionManager()