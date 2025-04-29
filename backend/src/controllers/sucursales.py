from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import SessionLocal
from services.sucursales import get_sucursales, get_sucursal, create_sucursal, update_sucursal, delete_sucursal
from api.schemas import SucursalCreate, SucursalUpdate
from typing import List

router = APIRouter(prefix="/sucursales", tags=["sucursales"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[dict])
def sucursales_get(db: Session = Depends(get_db)):
    sucursales = get_sucursales(db)
    return [{"id": s.id, "nombre": s.nombre, "zona": s.zona, "direccion": s.direccion, "superficie": s.superficie} for s in sucursales]

@router.get("/{sucursal_id}", response_model=dict)
def sucursal_get(sucursal_id: int, db: Session = Depends(get_db)):
    sucursal = get_sucursal(db, sucursal_id)
    return {"id": sucursal.id, "nombre": sucursal.nombre, "zona": sucursal.zona, "direccion": sucursal.direccion, "superficie": sucursal.superficie}

@router.post("/", response_model=dict)
def sucursal_create(sucursal: SucursalCreate, db: Session = Depends(get_db)):
    new_sucursal = create_sucursal(db, sucursal.nombre, sucursal.zona, sucursal.direccion, sucursal.superficie)
    return {"id": new_sucursal.id, "nombre": new_sucursal.nombre, "zona": new_sucursal.zona, "direccion": new_sucursal.direccion, "superficie": new_sucursal.superficie}

@router.put("/{sucursal_id}", response_model=dict)
def sucursal_update(sucursal_id: int, sucursal: SucursalUpdate, db: Session = Depends(get_db)):
    updated_sucursal = update_sucursal(db, sucursal_id, sucursal.nombre, sucursal.zona, sucursal.direccion, sucursal.superficie)
    return {"id": updated_sucursal.id, "nombre": updated_sucursal.nombre, "zona": updated_sucursal.zona, "direccion": updated_sucursal.direccion, "superficie": updated_sucursal.superficie}

@router.delete("/{sucursal_id}", response_model=dict)
def sucursal_delete(sucursal_id: int, db: Session = Depends(get_db)):
    return delete_sucursal(db, sucursal_id)