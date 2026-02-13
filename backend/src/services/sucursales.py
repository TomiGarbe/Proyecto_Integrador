from typing import Optional

from fastapi import HTTPException
from firebase_admin import db
from sqlalchemy.orm import Session

from api.models import Cliente, Sucursal
from auth.firebase import initialize_firebase

ALLOWED_FRECUENCIAS = {"Mensual", "Trimestral", "Cuatrimestral", "Semestral"}

def _ensure_usuario(current_entity: dict):
    if not current_entity:
        raise HTTPException(status_code=401, detail="Autenticación requerida")
    if current_entity.get("type") != "usuario":
        raise HTTPException(status_code=403, detail="No tienes permisos")

def _ensure_entity(current_entity: dict):
    if not current_entity:
        raise HTTPException(status_code=401, detail="Autenticación requerida")

def _validate_direccion(direccion: Optional[dict]):
    if not isinstance(direccion, dict):
        raise HTTPException(status_code=400, detail="El campo direccion debe ser un objeto con address, lat y lng")
    if "address" not in direccion:
        raise HTTPException(status_code=400, detail="El campo direccion debe incluir address")

def _validate_frecuencia(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    if value not in ALLOWED_FRECUENCIAS:
        raise HTTPException(status_code=400, detail="Frecuencia de preventivo inválida")
    return value

def _sync_firebase_sucursal(id_sucursal: int, nombre: str, direccion: Optional[dict]):
    if direccion is None:
        return
    try:
        initialize_firebase()
        ref = db.reference(f"/sucursales/{id_sucursal}")
        ref.set(
            {
                "name": nombre,
                "lat": direccion.get("lat", 0.0),
                "lng": direccion.get("lng", 0.0),
                "id_cliente": direccion.get("id_cliente"),
            }
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error guardando en Firebase: {str(exc)}")

def _update_firebase_sucursal(
    id_sucursal: int,
    nombre: Optional[str] = None,
    direccion: Optional[dict] = None,
    id_cliente: Optional[int] = None,
):
    updates = {}
    if nombre is not None:
        updates["name"] = nombre
    if direccion:
        if "lat" in direccion:
            updates["lat"] = direccion["lat"]
        if "lng" in direccion:
            updates["lng"] = direccion["lng"]
    if id_cliente is not None:
        updates["id_cliente"] = id_cliente
    if not updates:
        return
    try:
        initialize_firebase()
        ref = db.reference(f"/sucursales/{id_sucursal}")
        ref.update(updates)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error actualizando en Firebase: {str(exc)}")

def _delete_firebase_sucursal(id_sucursal: int):
    try:
        initialize_firebase()
        ref = db.reference(f"/sucursales/{id_sucursal}")
        ref.delete()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Error eliminando de Firebase: {str(exc)}")

def _get_cliente(db_session: Session, id_cliente: int) -> Cliente:
    cliente = db_session.query(Cliente).filter(Cliente.id == id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

def get_sucursales(db_session: Session, current_entity: dict):
    _ensure_entity(current_entity)
    return db_session.query(Sucursal).all()

def get_sucursal(db_session: Session, id_sucursal: int, current_entity: dict):
    _ensure_entity(current_entity)
    sucursal = db_session.query(Sucursal).filter(Sucursal.id == id_sucursal).first()
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return sucursal

def create_sucursal(
    db_session: Session,
    id_cliente: int,
    nombre: str,
    zona: str,
    direccion: dict,
    superficie: str,
    frecuencia_preventivo: Optional[str],
    current_entity: dict,
):
    _ensure_usuario(current_entity)
    _get_cliente(db_session, id_cliente)
    _validate_direccion(direccion)

    frecuencia = _validate_frecuencia(frecuencia_preventivo)
    sucursal = Sucursal(
        nombre=nombre,
        zona=zona,
        direccion=direccion.get("address", ""),
        superficie=superficie,
        id_cliente=id_cliente,
        frecuencia_preventivo=frecuencia,
    )
    try:
        db_session.add(sucursal)
        db_session.commit()
        db_session.refresh(sucursal)
    except Exception as exc:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Error guardando sucursal: {str(exc)}")

    _sync_firebase_sucursal(sucursal.id, nombre, {**direccion, "id_cliente": id_cliente})
    return sucursal

def update_sucursal(
    db_session: Session,
    id_sucursal: int,
    current_entity: dict,
    nombre: Optional[str] = None,
    zona: Optional[str] = None,
    direccion: Optional[dict] = None,
    superficie: Optional[str] = None,
    frecuencia_preventivo: Optional[str] = None,
    frecuencia_preventivo_provided: bool = False,
    id_cliente: Optional[int] = None,
):
    _ensure_usuario(current_entity)
    sucursal = get_sucursal(db_session, id_sucursal)

    if id_cliente is not None and id_cliente != sucursal.id_cliente:
        _get_cliente(db_session, id_cliente)
        sucursal.id_cliente = id_cliente
        cliente_changed = True
    else:
        cliente_changed = False

    if nombre is not None:
        sucursal.nombre = nombre
    if zona is not None:
        sucursal.zona = zona
    if direccion is not None:
        _validate_direccion(direccion)
        sucursal.direccion = direccion.get("address", "")
    if superficie is not None:
        sucursal.superficie = superficie
    if frecuencia_preventivo_provided:
        sucursal.frecuencia_preventivo = _validate_frecuencia(frecuencia_preventivo)

    try:
        db_session.commit()
        db_session.refresh(sucursal)
    except Exception as exc:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Error actualizando sucursal: {str(exc)}")

    cliente_value = sucursal.id_cliente if cliente_changed else None
    _update_firebase_sucursal(sucursal.id, nombre, direccion, cliente_value)
    return sucursal

def delete_sucursal(db_session: Session, id_sucursal: int, current_entity: dict):
    _ensure_usuario(current_entity)
    sucursal = get_sucursal(db_session, id_sucursal)

    try:
        db_session.delete(sucursal)
        db_session.commit()
    except Exception as exc:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Error eliminando sucursal: {str(exc)}")

    _delete_firebase_sucursal(id_sucursal)
    return {"message": f"Sucursal con id {id_sucursal} eliminada"}
