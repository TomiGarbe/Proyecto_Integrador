from sqlalchemy.orm import Session
from api.models import Cuadrilla
from fastapi import HTTPException

def _ensure_usuario(current_entity: dict):
    if not current_entity:
        raise HTTPException(status_code=401, detail="Autenticación requerida")
    if current_entity.get("type") != "usuario":
        raise HTTPException(status_code=403, detail="No tienes permisos")

def _ensure_entity(current_entity: dict):
    if not current_entity:
        raise HTTPException(status_code=401, detail="Autenticación requerida")

def get_cuadrillas(db: Session, current_entity: dict):
    _ensure_entity(current_entity)
    return db.query(Cuadrilla).all()

def get_cuadrilla(db: Session, cuadrilla_id: int, current_entity: dict):
    _ensure_entity(current_entity)
    cuadrilla = db.query(Cuadrilla).filter(Cuadrilla.id == cuadrilla_id).first()
    if not cuadrilla:
        raise HTTPException(status_code=404, detail="Cuadrilla no encontrada")
    return cuadrilla