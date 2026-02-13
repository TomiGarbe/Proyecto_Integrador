from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from config.database import get_db
from services.cuadrillas import get_cuadrillas, get_cuadrilla
from typing import List

router = APIRouter(prefix="/cuadrillas", tags=["cuadrillas"])

@router.get("/", response_model=List[dict])
async def cuadrillas_get(request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    cuadrillas = get_cuadrillas(db, current_entity)
    return [{"id": c.id, "nombre": c.nombre, "zona": c.zona, "email": c.email} for c in cuadrillas]

@router.get("/{id_cuadrilla}", response_model=dict)
async def cuadrilla_get(id_cuadrilla: int, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    cuadrilla = get_cuadrilla(db, id_cuadrilla, current_entity)
    return {"id": cuadrilla.id, "nombre": cuadrilla.nombre, "zona": cuadrilla.zona, "email": cuadrilla.email}