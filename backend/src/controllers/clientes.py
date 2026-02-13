from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from api.schemas import ClienteCreate, ClienteResponse, ClienteUpdate
from config.database import get_db
from services.clientes import (
    create_cliente,
    delete_cliente,
    get_cliente,
    get_clientes,
    update_cliente,
)

router = APIRouter(prefix="/clientes", tags=["clientes"])

@router.get("/", response_model=List[ClienteResponse])
def clientes_get(request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    clientes = get_clientes(db, current_entity)
    return clientes

@router.get("/{id_cliente}", response_model=ClienteResponse)
def cliente_get(id_cliente: int, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    return get_cliente(db, id_cliente, current_entity)

@router.post("/", response_model=ClienteResponse)
def cliente_create(cliente: ClienteCreate, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    return create_cliente(db, cliente.nombre, cliente.contacto, cliente.email, current_entity)

@router.put("/{id_cliente}", response_model=ClienteResponse)
def cliente_update(id_cliente: int, cliente: ClienteUpdate, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    return update_cliente(db, id_cliente, current_entity, cliente.nombre, cliente.contacto, cliente.email)

@router.delete("/{id_cliente}", response_model=dict)
def cliente_delete(id_cliente: int, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    return delete_cliente(db, id_cliente, current_entity)
