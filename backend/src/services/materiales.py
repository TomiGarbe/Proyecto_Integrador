from sqlalchemy.orm import Session
from fastapi import HTTPException
from api.models import Material, MovimientoStock

def _ensure_usuario(current_entity: dict):
    if not current_entity:
        raise HTTPException(status_code=401, detail="Autenticación requerida")
    if current_entity.get("type") != "usuario":
        raise HTTPException(status_code=403, detail="No tienes permisos")

def _ensure_entity(current_entity: dict):
    if not current_entity:
        raise HTTPException(status_code=401, detail="Autenticación requerida")

def get_materiales(db_session: Session, current_entity: dict):
    _ensure_entity(current_entity)
    return db_session.query(Material).all()

def get_material(db_session: Session, id: int, current_entity: dict):
    _ensure_entity(current_entity)
    return db_session.query(Material).filter(Material.id == id).first()

def get_movimientos(db_session: Session, current_entity: dict):
    _ensure_entity(current_entity)
    return db_session.query(MovimientoStock).all()

def get_movimiento(db_session: Session, id: int, current_entity: dict):
    _ensure_entity(current_entity)
    return db_session.query(MovimientoStock).filter(MovimientoStock.id == id).first()

def create_material(material: Material, db: Session, current_entity: dict):
    _ensure_usuario(current_entity)

    db_material = Material(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)

    return db_material

def registrar_movimiento(db: Session, movimiento:MovimientoStock, current_entity: dict):
    _ensure_entity(current_entity)

    material = db.query(Material).filter(Material.id == movimiento.id_material).first()
    if not material:
        raise HTTPException(status_code=404, detail="Material no encontrado")

    # ---- CONTROL STOCK ----
    if movimiento.tipo_movimiento == "egreso":
        if material.stock_actual < movimiento.cantidad:
            raise HTTPException(status_code=400, detail="Stock insuficiente")
        material.stock_actual -= movimiento.cantidad

    elif movimiento.tipo_movimiento == "ingreso":
        material.stock_actual += movimiento.cantidad

    elif movimiento.tipo_movimiento == "ajuste":
        material.stock_actual = movimiento.cantidad

    movimiento = MovimientoStock(**movimiento.dict())
    db.add(movimiento)
    db.commit()
    db.refresh(movimiento)

    return movimiento

def update_material(db: Session, id: int, material: Material, current_entity: dict):
    _ensure_usuario(current_entity)
    db_material = db.query(Material).filter(Material.id == id).first()
    if not db_material:
        raise HTTPException(status_code=404, detail="Material no encontrado")
    for key, value in material.dict(exclude_unset=True).items():
        setattr(db_material, key, value)
    db.commit()
    return db_material

def update_movimiento(db: Session, id: int, movimiento: MovimientoStock, current_entity: dict):
    _ensure_usuario(current_entity)
    db_movimiento = db.query(MovimientoStock).filter(MovimientoStock.id == id).first()
    if not db_movimiento:
        raise HTTPException(status_code=404, detail="Movimiento no encontrado")
    for key, value in movimiento.dict(exclude_unset=True).items():
        setattr(db_movimiento, key, value)
    db.commit()
    db.refresh(db_movimiento)

    return db_movimiento
