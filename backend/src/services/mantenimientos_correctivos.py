from datetime import date, datetime
from typing import List, Optional
import os

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from api.models import Cliente, Cuadrilla, Obra, MantenimientoCorrectivo, FotoObra, Sucursal
from services.gcloud_storage import delete_file_in_folder, upload_file_to_gcloud
from services.google_sheets import append_correctivo, delete_correctivo, update_correctivo
from services.notificaciones import notify_user, notify_users

GOOGLE_CLOUD_BUCKET_NAME = os.getenv("GOOGLE_CLOUD_BUCKET_NAME")

def _ensure_usuario(current_entity: dict):
    if not current_entity:
        raise HTTPException(status_code=401, detail="Autenticación requerida")
    if current_entity.get("type") != "usuario":
        raise HTTPException(status_code=403, detail="No tienes permisos")

def _ensure_entity(current_entity: dict):
    if not current_entity:
        raise HTTPException(status_code=401, detail="Autenticación requerida")

def _get_cliente(db: Session, id_cliente: int) -> Cliente:
    cliente = db.query(Cliente).filter(Cliente.id == id_cliente).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

def _get_sucursal(db: Session, id_sucursal: int) -> Sucursal:
    sucursal = db.query(Sucursal).filter(Sucursal.id == id_sucursal).first()
    if not sucursal:
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return sucursal

def _ensure_cliente_sucursal(id_cliente: int, sucursal: Sucursal):
    if sucursal.id_cliente != id_cliente:
        raise HTTPException(status_code=400, detail="La sucursal no pertenece al cliente seleccionado")

def _get_cuadrilla(db: Session, id_cuadrilla: int) -> Cuadrilla:
    cuadrilla = db.query(Cuadrilla).filter(Cuadrilla.id == id_cuadrilla).first()
    if not cuadrilla:
        raise HTTPException(status_code=404, detail="Cuadrilla no encontrada")
    return cuadrilla

def _get_fotos(db: Session, id_obra: int) -> List[FotoObra]:
    fotos = db.query(FotoObra).filter(FotoObra.id_obra == id_obra).all()
    return fotos

def get_mantenimientos_correctivos(db: Session, current_entity: dict):
    _ensure_entity(current_entity)
    return db.query(MantenimientoCorrectivo).all()

def get_mantenimiento_correctivo(db: Session, id_mantenimiento: int, current_entity: dict):
    _ensure_entity(current_entity)
    mantenimiento = (
        db.query(MantenimientoCorrectivo)
        .filter(MantenimientoCorrectivo.id == id_mantenimiento)
        .first()
    )
    if not mantenimiento:
        raise HTTPException(status_code=404, detail="Mantenimiento correctivo no encontrado")
    fotos = _get_fotos(db, mantenimiento.id_obra)
    return mantenimiento, fotos

async def create_mantenimiento_correctivo(
    db: Session,
    id_cliente: int,
    id_sucursal: int,
    id_cuadrilla: Optional[int],
    fecha_apertura: date,
    numero_caso: str,
    incidente: str,
    rubro: str,
    estado: str,
    prioridad: str,
    current_entity: dict,
):
    _ensure_usuario(current_entity)

    cliente = _get_cliente(db, id_cliente)
    sucursal = _get_sucursal(db, id_sucursal)
    _ensure_cliente_sucursal(id_cliente, sucursal)

    cuadrilla = _get_cuadrilla(db, id_cuadrilla) if id_cuadrilla else None

    obra = Obra(tipo="correctivo")
    db.add(obra)
    db.flush()

    db_mantenimiento = MantenimientoCorrectivo(
        id_obra=obra.id,
        id_cliente=id_cliente,
        id_sucursal=id_sucursal,
        id_cuadrilla=id_cuadrilla,
        fecha_apertura=fecha_apertura,
        numero_caso=numero_caso,
        incidente=incidente,
        rubro=rubro,
        estado=estado,
        prioridad=prioridad,
    )
    db.add(db_mantenimiento)
    db.commit()
    db.refresh(db_mantenimiento)
    append_correctivo(db_mantenimiento)
    
    if cuadrilla is not None:
        if prioridad == "Alta":
            notify_user(
                db_session=db,
                firebase_uid=cuadrilla.firebase_uid,
                id_obra=obra.id,
                mensaje=f"Nuevo correctivo asignado - Sucursal: {sucursal.nombre} | Incidente: {db_mantenimiento.incidente} | Prioridad: {db_mantenimiento.prioridad}",
                title="Nuevo correctivo urgente asignado",
                body=f"Sucursal: {sucursal.nombre} | Incidente: {db_mantenimiento.incidente}",
            )
        await notify_users(
            db_session=db,
            id_obra=obra.id,
            mensaje=f"Nuevo correctivo asignado - Sucursal: {sucursal.nombre} | Incidente: {db_mantenimiento.incidente} | Prioridad: {db_mantenimiento.prioridad}",
            firebase_uid=cuadrilla.firebase_uid,
        )
    return db_mantenimiento

async def update_mantenimiento_correctivo(
    db: Session,
    id_mantenimiento: int,
    current_entity: dict,
    id_cliente: Optional[int] = None,
    id_sucursal: Optional[int] = None,
    id_cuadrilla: Optional[int] = None,
    fecha_apertura: Optional[date] = None,
    fecha_cierre: Optional[date] = None,
    numero_caso: Optional[str] = None,
    incidente: Optional[str] = None,
    rubro: Optional[str] = None,
    planilla: Optional[UploadFile] = None,
    fotos: Optional[List[UploadFile]] = None,
    estado: Optional[str] = None,
    prioridad: Optional[str] = None,
    extendido: Optional[datetime] = None,
):
    _ensure_entity(current_entity)

    db_mantenimiento = db.query(MantenimientoCorrectivo).filter(MantenimientoCorrectivo.id == id_mantenimiento).first()

    if not db_mantenimiento:
        raise HTTPException(status_code=404, detail="Mantenimiento correctivo no encontrado")

    bucket_name = GOOGLE_CLOUD_BUCKET_NAME
    if not bucket_name:
        raise HTTPException(status_code=500, detail="Google Cloud Bucket name not configured")
    base_folder = f"obras/{db_mantenimiento.id_obra}"

    final_id_cliente = id_cliente if id_cliente is not None else db_mantenimiento.id_cliente
    final_id_sucursal = id_sucursal if id_sucursal is not None else db_mantenimiento.id_sucursal
    cliente = _get_cliente(db, final_id_cliente)
    sucursal = _get_sucursal(db, final_id_sucursal)
    _ensure_cliente_sucursal(cliente.id, sucursal)

    db_mantenimiento.id_cliente = cliente.id
    db_mantenimiento.id_sucursal = sucursal.id

    if fecha_apertura is not None:
        db_mantenimiento.fecha_apertura = fecha_apertura
    if numero_caso is not None:
        db_mantenimiento.numero_caso = numero_caso
    if incidente is not None:
        db_mantenimiento.incidente = incidente
    if rubro is not None:
        db_mantenimiento.rubro = rubro

    if id_cuadrilla:
        cuadrilla = _get_cuadrilla(db, id_cuadrilla)
        db_mantenimiento.id_cuadrilla = id_cuadrilla
    else:
        cuadrilla = _get_cuadrilla(db, db_mantenimiento.id_cuadrilla) if db_mantenimiento.id_cuadrilla else None

    if planilla is not None:
        planilla_url = await upload_file_to_gcloud(planilla, bucket_name, f"{base_folder}/planilla")
        db_mantenimiento.planilla = planilla_url

    if fotos is not None:
        for foto in fotos:
            url = await upload_file_to_gcloud(foto, bucket_name, f"{base_folder}/fotos")
            new_foto = FotoObra(id_obra=db_mantenimiento.id_obra, url=url)
            db.add(new_foto)

    if fecha_cierre is not None:
        if fecha_cierre == date(1, 1, 1):
            db_mantenimiento.fecha_cierre = None
        else:
            db_mantenimiento.fecha_cierre = fecha_cierre

    if estado is not None:
        db_mantenimiento.estado = estado
        if estado not in ("Solucionado", "Finalizado"):
            db_mantenimiento.fecha_cierre = None
        if estado == "Solucionado":
            await notify_users(
                db_session=db,
                id_obra=db_mantenimiento.id_obra,
                mensaje=f"Correctivo Solucionado - Sucursal: {sucursal.nombre} | Incidente: {db_mantenimiento.incidente}",
                firebase_uid=None,
            )

    if prioridad is not None:
        db_mantenimiento.prioridad = prioridad

    prioridad_actual = prioridad if prioridad is not None else db_mantenimiento.prioridad

    if extendido is not None:
        db_mantenimiento.extendido = extendido
        if cuadrilla:
            await notify_users(
                db_session=db,
                id_obra=db_mantenimiento.id_obra,
                mensaje=f"Extendido solicitado - Sucursal: {sucursal.nombre} | Cuadrilla: {cuadrilla.nombre}",
                firebase_uid=None,
            )

    db.commit()
    db.refresh(db_mantenimiento)
    update_correctivo(db_mantenimiento)

    if cuadrilla is not None and prioridad_actual == "Alta":
        notify_user(
            db_session=db,
            firebase_uid=cuadrilla.firebase_uid,
            id_obra=db_mantenimiento.id_obra,
            mensaje=f"Correctivo urgente asignado - Sucursal: {sucursal.nombre} | Incidente: {db_mantenimiento.incidente} | Prioridad: {db_mantenimiento.prioridad}",
            title="Correctivo urgente asignado",
            body=f"Sucursal: {sucursal.nombre} | Incidente: {db_mantenimiento.incidente}",
        )
        await notify_users(
            db_session=db,
            id_obra=db_mantenimiento.id_obra,
            mensaje=f"Correctivo urgente asignado - Sucursal: {sucursal.nombre} | Incidente: {db_mantenimiento.incidente} | Prioridad: {db_mantenimiento.prioridad}",
            firebase_uid=cuadrilla.firebase_uid,
        )
    
    fotos = _get_fotos(db, db_mantenimiento.id_obra)

    return db_mantenimiento, fotos

def delete_mantenimiento_correctivo(db: Session, id_mantenimiento: int, current_entity: dict):
    _ensure_usuario(current_entity)
    
    db_mantenimiento = db.query(MantenimientoCorrectivo).filter(MantenimientoCorrectivo.id == id_mantenimiento).first()

    if not db_mantenimiento:
        raise HTTPException(status_code=404, detail="Mantenimiento correctivo no encontrado")

    db_obra = db.query(Obra).filter(Obra.id == db_mantenimiento.id_obra).first()
    db.delete(db_mantenimiento)
    db.delete(db_obra)
    db.commit()
    delete_correctivo(id_mantenimiento)
    return {"message": f"Mantenimiento correctivo con id {id_mantenimiento} eliminado"}
