from fastapi import HTTPException
from sqlalchemy.orm import Session
from api.models import Notificacion, Usuario
from .webpush import send_webpush_notification
from .notification_ws import notification_manager
from datetime import datetime, timezone, timedelta
from typing import Optional
    
def notify_user(db_session: Session, firebase_uid: str, id_obra: int, mensaje: str, title: str, body: str):
    now_utc = datetime.now(timezone.utc)
    today_start = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    existing_notification = db_session.query(Notificacion).filter(
        Notificacion.firebase_uid == firebase_uid,
        Notificacion.id_obra == id_obra,
        Notificacion.mensaje == mensaje,
        Notificacion.created_at >= today_start,
        Notificacion.created_at <= today_end
    ).first()
    if not existing_notification:
        send_webpush_notification(db_session, firebase_uid, title, body)
        return {"message": "Notification sent"}
    return {"message": "Notification already sent"}

def get_notification(db_session: Session, firebase_uid: str):
    return db_session.query(Notificacion).filter(Notificacion.firebase_uid == firebase_uid).all()

def notificacion_leida(db_session: Session, id_notificacion: int):
    db_notificacion = db_session.query(Notificacion).filter(Notificacion.id == id_notificacion).first()
    db_notificacion.leida = True
    db_session.commit()
    db_session.refresh(db_notificacion)
    return db_notificacion

async def send_notification(db_session: Session, firebase_uid: str, id_obra: int, mensaje: str):
    now_utc = datetime.now(timezone.utc)
    today_start = now_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    existing_notification = db_session.query(Notificacion).filter(
        Notificacion.firebase_uid == firebase_uid,
        Notificacion.id_obra == id_obra,
        Notificacion.mensaje == mensaje,
        Notificacion.created_at >= today_start,
        Notificacion.created_at <= today_end
    ).first()
    if not existing_notification:
        db_notificacion = Notificacion(firebase_uid=firebase_uid, id_obra=id_obra, mensaje=mensaje)
        db_session.add(db_notificacion)
        db_session.commit()
        db_session.refresh(db_notificacion)
        await notification_manager.send_notification(
            firebase_uid,
            {
                "id": db_notificacion.id,
                "firebase_uid": firebase_uid,
                "id_obra": id_obra,
                "mensaje": mensaje,
                "leida": db_notificacion.leida,
                "created_at": db_notificacion.created_at.isoformat(),
                "tipo": "correctivo",
            },
        )
        return True
    return False

async def notify_users(db_session: Session, id_obra: int, mensaje: str, firebase_uid: Optional[str] = None):
    if firebase_uid is not None:
        await send_notification(db_session, firebase_uid, id_obra, mensaje)
    else:
        encargados = db_session.query(Usuario).filter(Usuario.rol == "Encargado de Mantenimiento").all()
        for encargado in encargados:
            await send_notification(db_session, encargado.firebase_uid, id_obra, mensaje)
        if "Solucionado" in mensaje:
            admins = db_session.query(Usuario).filter(Usuario.rol == "Administrador").all()
            for admin in admins:
                await send_notification(db_session, admin.firebase_uid, id_obra, mensaje)

async def notify_nearby_maintenances(db_session: Session, current_entity: dict, mantenimientos: list[dict]):
    if not current_entity:
        raise HTTPException(status_code=401, detail="Autenticación requerida")
    firebase_uid = current_entity["data"]["uid"]
    for m in mantenimientos:
        created = await send_notification(db_session, firebase_uid, m['id_obra'], m.get('mensaje', ''))
        if created:
            send_webpush_notification(db_session, firebase_uid, 'Mantenimiento cercano', m.get('mensaje', ''))
    return {"message": "Notificaciones enviadas"}

def delete_notificaciones(db_session: Session, firebase_uid: str):
    db_session.query(Notificacion).filter(Notificacion.firebase_uid == firebase_uid).delete()
    db_session.commit()
    return {"message": "Notificaciones eliminadas"}

def delete_notificacion(db_session: Session, id_notificacion: int):
    notification = db_session.query(Notificacion).filter(Notificacion.id == id_notificacion).first()
    if notification:
        db_session.delete(notification)
        db_session.commit()
        return {"detail": "Notificación eliminada"}

    return {"detail": "No se encontró la notificación"}