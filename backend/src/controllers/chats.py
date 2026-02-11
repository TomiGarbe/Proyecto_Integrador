from fastapi import APIRouter, Depends, Request, UploadFile, Form, File
from sqlalchemy.orm import Session
from config.database import get_db
from services.chats import get_chat, send_message
from typing import List, Optional

router = APIRouter(prefix="/chat", tags=["chat"])

@router.get("/{id_obra}", response_model=List[dict])
def chat_get(id_obra: int, request: Request, db_session: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    chat = get_chat(db_session, id_obra, current_entity)
    if isinstance(chat, dict):
        return []
    return [
        {
            "id": message.id,
            "firebase_uid": message.firebase_uid,
            "nombre_usuario": message.nombre_usuario,
            "id_obra": message.id_obra,
            "texto": message.texto,
            "archivo": message.archivo,
            "fecha": message.created_at,
        }
        for message in chat
    ]

@router.post("/message/{id_obra}", response_model=dict)
async def message_send(
    id_obra: int,
    request: Request,
    firebase_uid: str = Form(...),
    nombre_usuario: str = Form(...),
    texto: Optional[str] = Form(None),
    archivo: Optional[UploadFile] = File(None),
    db_session: Session = Depends(get_db)
):
    current_entity = request.state.current_entity
    new_message = await send_message(
        db_session,
        id_obra,
        firebase_uid,
        nombre_usuario,
        current_entity,
        texto,
        archivo
    )
    return {
        "id": new_message.id,
        "firebase_uid": new_message.firebase_uid,
        "nombre_usuario": new_message.nombre_usuario,
        "id_obra": new_message.id_obra,
        "texto": new_message.texto,
        "archivo": new_message.archivo,
        "fecha": new_message.created_at
    }
