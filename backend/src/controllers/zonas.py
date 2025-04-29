from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import SessionLocal
from services.zonas import get_zonas, create_zona, delete_zona
from api.schemas import Zona
from typing import List

router = APIRouter(prefix="/zonas", tags=["zonas"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@router.get("/", response_model=List[dict])
def zonas_get(db: Session = Depends(get_db)):
    zonas = get_zonas(db)
    return [{"id": z.id, "nombre": z.nombre} for z in zonas]

@router.post("/", response_model=dict)
def zona_create(zona: Zona, db: Session = Depends(get_db)):
    new_zona = create_zona(db, zona.nombre)
    return {"id": new_zona.id, "nombre": new_zona.nombre}

@router.delete("/{id}", response_model=dict)
def zona_delete(id: int, db: Session = Depends(get_db)):
    return delete_zona(db, id)