from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import MaterialCreate, MovimientoStockCreate
from app.services.materiales import create_material, get_materiales, registrar_movimiento
from app.models import Material

router = APIRouter(prefix="/materiales", tags=["Materiales"])

@router.post("/", response_model=MaterialCreate)
def material_create(material: MaterialCreate, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    return new_material = create_material(material, current_entity, db)

@router.get("/", response_model=list[MaterialCreate])
def materiales_get(request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    return get_materiales(db, current_entity)

@router.post("/movimientos", response_model=MovimientoStockCreate)
def crear_movimiento(movimiento: MovimientoCreate, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    return registrar_movimiento(db, movimiento, current_entity)
