from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from config.database import get_db
from services.notificaciones import get_notification, notificacion_leida, delete_notificaciones, notify_nearby_maintenances, delete_notificacion
from typing import List
from api.schemas import NearbyNotificationCreate

router = APIRouter(prefix="/notificaciones", tags=["notificaciones"])

@router.get("/{firebase_uid}", response_model=List[dict])
def notificaciones_get(firebase_uid: str, db: Session = Depends(get_db)):
    notificaciones = get_notification(db, firebase_uid)
    return [{"id": n.id, "firebase_uid": n.firebase_uid, "id_obra": n.id_obra, "mensaje": n.mensaje, "leida": n.leida, "created_at": n.created_at} for n in notificaciones]

@router.put("/{id_notificacion}", response_model=dict)
def notificacion_leida(id_notificacion: int, db: Session = Depends(get_db)):
    notificacion = notificacion_leida(db, id_notificacion)
    return {"id": notificacion.id, "firebase_uid": notificacion.firebase_uid, "id_obra": notificacion.id_obra, "mensaje": notificacion.mensaje, "leida": notificacion.leida, "created_at": notificacion.created_at}

@router.delete("/{firebase_uid}", response_model=dict)
def notificaciones_delete(firebase_uid: str, db: Session = Depends(get_db)):
    return delete_notificaciones(db, firebase_uid)

@router.post("/nearby", response_model=dict)
async def notificaciones_nearby(payload: NearbyNotificationCreate, request: Request, db: Session = Depends(get_db)):
    current = request.state.current_entity
    return await notify_nearby_maintenances(db, current, [m.model_dump() for m in payload.mantenimientos])

@router.delete("/delete/{id_notificacion}", response_model=dict)
def notificacion_delete(id_notificacion: int, db: Session = Depends(get_db)):
    return delete_notificacion(db, id_notificacion)
