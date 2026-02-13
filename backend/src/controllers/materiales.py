from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import MaterialCreate, MovimientoStockCreate
from app.services.materiales import get_materiales, get_material, get_movimientos, get_movimiento, create_material, registrar_movimiento, update_material, update_movimiento
from app.models import Material

router = APIRouter(prefix="/materiales", tags=["Materiales"])

@router.get("/", response_model=list[MaterialCreate])
def materiales_get(request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    return get_materiales(db, current_entity)

@router.get("/{id}", response_model=MaterialCreate)
def material_get(id: int, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    return get_material(db, id, current_entity)

@router.get("/movimientos", response_model=list[MovimientoStockCreate])
def movimientos_get(request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    return get_movimientos(db, current_entity)

@router.get("/movimientos/{id}", response_model=MovimientoStockCreate)
def movimiento_get(id: int, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    return get_movimiento(db, id, current_entity)

@router.post("/", response_model=MaterialCreate)
def material_create(material: MaterialCreate, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    return new_material = create_material(material, current_entity, db)

@router.post("/movimientos", response_model=MovimientoStockCreate)
def crear_movimiento(movimiento: MovimientoCreate, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    return registrar_movimiento(db, movimiento, current_entity)

@router.put("/{id}", response_model=MaterialCreate)
def material_update(id: int, material: MaterialCreate, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    return update_material(db, id, material, current_entity)

@router.put("/movimientos/{id}", response_model=MovimientoStockCreate)
def movimiento_update(id: int, movimiento: MovimientoStockCreate, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    return update_movimiento(db, id, movimiento, current_entity)
