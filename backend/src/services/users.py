from sqlalchemy.orm import Session
from api.models import Usuario
from fastapi import HTTPException
from api.schemas import Role

def _ensure_admin(current_entity: dict):
    if not current_entity:
        raise HTTPException(status_code=401, detail="Autenticación requerida")
    if current_entity["type"] != "usuario" or current_entity["data"]["rol"] != Role.ADMIN:
        raise HTTPException(status_code=403, detail="No tienes permisos de administrador")

def _ensure_entity(current_entity: dict):
    if not current_entity:
        raise HTTPException(status_code=401, detail="Autenticación requerida")

def get_users(db: Session, current_entity: dict):
    _ensure_admin(current_entity)
    return db.query(Usuario).all()

def get_user(db: Session, id_user: int, current_entity: dict):
    _ensure_entity(current_entity)
    user = db.query(Usuario).filter(Usuario.id == id_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if current_entity["type"] != "usuario" or (current_entity["data"]["rol"] != Role.ADMIN and current_entity["data"]["id"] != id_user):
        raise HTTPException(status_code=403, detail="No tienes permisos para ver este usuario")
    return user