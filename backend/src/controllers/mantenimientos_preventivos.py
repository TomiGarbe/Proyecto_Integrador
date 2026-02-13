from fastapi import APIRouter, Depends, Request, UploadFile, Form
from sqlalchemy.orm import Session
from config.database import get_db
from services.mantenimientos_preventivos import get_mantenimientos_preventivos, get_mantenimiento_preventivo, create_mantenimiento_preventivo, update_mantenimiento_preventivo, delete_mantenimiento_preventivo
from api.schemas import MantenimientoPreventivoCreate
from typing import List, Optional
from datetime import date, datetime

router = APIRouter(prefix="/mantenimientos-preventivos", tags=["mantenimientos-preventivos"])

@router.get("/", response_model=List[dict])
def mantenimientos_preventivos_get(request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    mantenimientos = get_mantenimientos_preventivos(db, current_entity)
    return [
        {
            "id": m.id,
            "id_obra": m.id_obra,
            "id_cliente": m.id_cliente,
            "id_sucursal": m.id_sucursal,
            "frecuencia": m.frecuencia,
            "id_cuadrilla": m.id_cuadrilla,
            "fecha_apertura": m.fecha_apertura,
            "fecha_cierre": m.fecha_cierre,
            "planillas": [planilla.url for planilla in m.planillas],
            "fotos": [foto.url for foto in m.fotos],
            "extendido": m.extendido,
            "estado": m.estado
        }
        for m in mantenimientos
    ]

@router.get("/{id_mantenimiento}", response_model=dict)
def mantenimiento_preventivo_get(id_mantenimiento: int, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    mantenimiento = get_mantenimiento_preventivo(db, id_mantenimiento, current_entity)
    return {
        "id": mantenimiento.id,
        "id_obra": mantenimiento.id_obra,
        "id_cliente": mantenimiento.id_cliente,
        "id_sucursal": mantenimiento.id_sucursal,
        "frecuencia": mantenimiento.frecuencia,
        "id_cuadrilla": mantenimiento.id_cuadrilla,
        "fecha_apertura": mantenimiento.fecha_apertura,
        "fecha_cierre": mantenimiento.fecha_cierre,
        "planillas": [planilla.url for planilla in mantenimiento.planillas],
        "fotos": [foto.url for foto in mantenimiento.fotos],
        "extendido": mantenimiento.extendido,
        "estado": mantenimiento.estado
    }

@router.post("/", response_model=dict)
async def mantenimiento_preventivo_create(mantenimiento: MantenimientoPreventivoCreate, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    new_mantenimiento = await create_mantenimiento_preventivo(
        db,
        mantenimiento.id_cliente,
        mantenimiento.id_sucursal,
        mantenimiento.frecuencia.value,
        mantenimiento.id_cuadrilla,
        mantenimiento.fecha_apertura,
        mantenimiento.estado,
        current_entity
    )
    return {
        "id": new_mantenimiento.id,
        "id_obra": new_mantenimiento.id_obra,
        "id_cliente": new_mantenimiento.id_cliente,
        "id_sucursal": new_mantenimiento.id_sucursal,
        "frecuencia": new_mantenimiento.frecuencia,
        "id_cuadrilla": new_mantenimiento.id_cuadrilla,
        "fecha_apertura": new_mantenimiento.fecha_apertura,
        "estado": new_mantenimiento.estado
    }

@router.put("/{id_mantenimiento}", response_model=dict)
async def mantenimiento_preventivo_update(
    id_mantenimiento: int,
    request: Request,
    id_cliente: Optional[int] = Form(None),
    id_sucursal: Optional[int] = Form(None),
    frecuencia: Optional[str] = Form(None),
    id_cuadrilla: Optional[int] = Form(None),
    fecha_apertura: Optional[date] = Form(None),
    fecha_cierre: Optional[date] = Form(None),
    planillas: Optional[List[UploadFile]] = None,
    fotos: Optional[List[UploadFile]] = None,
    extendido: Optional[datetime] = Form(None),
    estado: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    current_entity = request.state.current_entity
    updated_mantenimiento = await update_mantenimiento_preventivo(
        db,
        id_mantenimiento,
        current_entity,
        id_cliente,
        id_sucursal,
        frecuencia,
        id_cuadrilla,
        fecha_apertura,
        fecha_cierre,
        planillas,
        fotos,
        extendido,
        estado
    )
    return {
        "id": updated_mantenimiento.id,
        "id_obra": updated_mantenimiento.id_obra,
        "id_cliente": updated_mantenimiento.id_cliente,
        "id_sucursal": updated_mantenimiento.id_sucursal,
        "frecuencia": updated_mantenimiento.frecuencia,
        "id_cuadrilla": updated_mantenimiento.id_cuadrilla,
        "fecha_apertura": updated_mantenimiento.fecha_apertura,
        "fecha_cierre": updated_mantenimiento.fecha_cierre,
        "planillas": [planilla.url for planilla in updated_mantenimiento.planillas],
        "fotos": [foto.url for foto in updated_mantenimiento.fotos],
        "extendido": updated_mantenimiento.extendido,
        "estado": updated_mantenimiento.estado
    }

@router.delete("/{id_mantenimiento}", response_model=dict)
def mantenimiento_preventivo_delete(id_mantenimiento: int, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    return delete_mantenimiento_preventivo(db, id_mantenimiento, current_entity)
