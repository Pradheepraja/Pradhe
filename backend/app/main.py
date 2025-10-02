from __future__ import annotations
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db import Base, engine
from .utils.notifications import connection_manager
from .auth import decode_access_token

from .routers import auth as auth_router


app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


# Routers
app.include_router(auth_router.router, prefix="/auth", tags=["auth"])


# WebSocket for real-time nudges
@app.websocket("/ws")
async def notifications_ws(websocket: WebSocket) -> None:
    token: Optional[str] = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=4401)
        return
    payload = decode_access_token(token)
    if not payload or payload.get("sub") is None:
        await websocket.close(code=4401)
        return
    user_id = int(payload["sub"])

    await connection_manager.connect(user_id, websocket)
    try:
        while True:
            # Keep the connection alive by receiving any ping/pong
            await websocket.receive_text()
    except WebSocketDisconnect:
        connection_manager.disconnect(user_id, websocket)
