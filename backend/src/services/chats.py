from sqlalchemy.orm import Session
from api.models import Mensaje
from fastapi import HTTPException, UploadFile
from typing import Optional
from services.gcloud_storage import upload_chat_file_to_gcloud
from services.chat_ws import chat_manager
import os

GOOGLE_CLOUD_BUCKET_NAME = os.getenv("GOOGLE_CLOUD_BUCKET_NAME")

def _ensure_entity(current_entity: dict):
    if not current_entity:
        raise HTTPException(status_code=401, detail="Autenticación requerida")

def get_chat(db_session: Session, id_obra: int, current_entity: dict):
    _ensure_entity(current_entity)

    chat = db_session.query(Mensaje).filter(Mensaje.id_obra == id_obra).all()
    if not chat:
        return {"message": "No hay mensajes"}
    return chat

async def send_message(
    db_session: Session,
    id_obra: int,
    firebase_uid: str,
    nombre_usuario: str,
    current_entity: dict,
    texto: Optional[str] = None,
    archivo: Optional[UploadFile] = None,
    ):
    _ensure_entity(current_entity)
    
    bucket_name = GOOGLE_CLOUD_BUCKET_NAME
    if not bucket_name:
        raise HTTPException(status_code=500, detail="Google Cloud Bucket name not configured")
    
    try:
        base_folder = f"mensajes/{id_obra}"
        db_message = Mensaje(
            firebase_uid=firebase_uid,
            nombre_usuario=nombre_usuario,
            id_obra=id_obra
        )
        if texto is not None:
            db_message.texto = texto
        if archivo is not None:
            archivo_url = await upload_chat_file_to_gcloud(archivo, bucket_name, f"{base_folder}/chat")
            db_message.archivo = archivo_url
        
        db_session.add(db_message)
        db_session.commit()
        db_session.refresh(db_message)
        await chat_manager.send_message(
            id_obra,
            {
                "id": db_message.id,
                "firebase_uid": db_message.firebase_uid,
                "nombre_usuario": db_message.nombre_usuario,
                "id_obra": db_message.id_obra,
                "texto": db_message.texto,
                "archivo": db_message.archivo,
                "fecha": db_message.created_at.isoformat() if db_message.created_at else None,
            },
        )
        return db_message
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
