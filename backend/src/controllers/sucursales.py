from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from api.schemas import SucursalCreate, SucursalUpdate
from config.database import get_db
from services.sucursales import (
    create_sucursal,
    delete_sucursal,
    get_sucursales,
    get_sucursal,
    update_sucursal,
)

router = APIRouter(tags=["sucursales"])

def _serialize_sucursal(s) -> dict:
    return {
        "id": s.id,
        "nombre": s.nombre,
        "zona": s.zona,
        "direccion": s.direccion,
        "superficie": s.superficie,
        "id_cliente": s.id_cliente,
        "frecuencia_preventivo": s.frecuencia_preventivo,
    }

@router.get("/", response_model=List[dict])
def sucursales_get(request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    sucursales = get_sucursales(db, current_entity)
    return [_serialize_sucursal(s) for s in sucursales]

@router.get("/{id_sucursal}", response_model=dict)
def sucursal_get(id_sucursal: int, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    sucursal = get_sucursal(db, id_sucursal, current_entity)
    return _serialize_sucursal(sucursal)

@router.post("/", response_model=dict)
def sucursal_create(id_cliente: int, sucursal: SucursalCreate, request: Request, db: Session = Depends(get_db)):
    if sucursal.id_cliente != id_cliente:
        raise HTTPException(status_code=400, detail="El cliente del cuerpo no coincide con el de la ruta")
    current_entity = request.state.current_entity
    new_sucursal = create_sucursal(
        db,
        id_cliente,
        sucursal.nombre,
        sucursal.zona,
        sucursal.direccion,
        sucursal.superficie,
        sucursal.frecuencia_preventivo.value if sucursal.frecuencia_preventivo else None,
        current_entity,
    )
    return _serialize_sucursal(new_sucursal)

@router.put("/{id_sucursal}", response_model=dict)
def sucursal_update(id_sucursal: int, sucursal: SucursalUpdate, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    freq_provided = "frecuencia_preventivo" in sucursal.__fields_set__
    freq_value = sucursal.frecuencia_preventivo.value if sucursal.frecuencia_preventivo else None
    updated_sucursal = update_sucursal(
        db,
        id_sucursal,
        current_entity,
        sucursal.nombre,
        sucursal.zona,
        sucursal.direccion,
        sucursal.superficie,
        freq_value,
        freq_provided,
        sucursal.id_cliente,
    )
    return _serialize_sucursal(updated_sucursal)

@router.delete("/{id_sucursal}", response_model=dict)
def sucursal_delete(id_sucursal: int, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    return delete_sucursal(db, id_sucursal, current_entity)
