from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from config.database import get_db
from pydantic import BaseModel
from typing import List
from services.maps import get_sucursales_locations, get_users_locations, get_selection, update_user_location, update_selection, delete_sucursal, delete_obra, delete_selection
from api.models import Cuadrilla
import os

router = APIRouter(prefix="/maps", tags=["maps"])

class LocationUpdate(BaseModel):
    lat: float
    lng: float
    name: str

class Seleccion(BaseModel):
    id_mantenimiento: int
    id_sucursal: int

@router.get("/sucursales-locations", response_model=List[dict])
async def locations_get(request: Request):
    current_entity = request.state.current_entity
    sucursales = await get_sucursales_locations(current_entity)
    return [{"id": s.id, "name": s.name, "lat": s.lat, "lng": s.lng} for s in sucursales]

@router.get("/users-locations", response_model=List[dict])
async def locations_get(request: Request):
    current_entity = request.state.current_entity
    users = await get_users_locations(current_entity)
    return [{"id": u.id, "tipo": u.tipo, "name": u.name, "lat": u.lat, "lng": u.lng} for u in users]

@router.get("/selection/{id_cuadrilla}", response_model=List[dict])
def selection_get(request: Request, id_cuadrilla: int = None, db_session: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    obras_ids = get_selection(db_session, id_cuadrilla, current_entity)
    return [{"id_mantenimiento": o.id_mantenimiento, "id_sucursal": o.id_sucursal} for o in obras_ids]

@router.post("/update-user-location", response_model=dict)
async def location_update(request: Request, location: LocationUpdate, db_session: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    if os.environ.get("E2E_TESTING") == "true":
        cuadrilla = db_session.query(Cuadrilla).filter(Cuadrilla.nombre == "Cuadrilla E2E").first()
        firebase_uid = cuadrilla.firebase_uid
        id_user = str(cuadrilla.id)
        tipo = "cuadrilla"
    else:
        firebase_uid = str(current_entity["data"]["uid"])
        id_user = str(current_entity["data"]["id"])
        if current_entity["type"] == "usuario":
            tipo = str(current_entity["data"]["rol"])
        else:
            tipo = str(current_entity["type"])
    return await update_user_location(current_entity, firebase_uid, id_user, tipo, location.name, location.lat, location.lng)

@router.post("/select-obra", response_model=dict)
def selection_update(request: Request, s: Seleccion, db_session: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    if os.environ.get("E2E_TESTING") == "true":
        cuadrilla = db_session.query(Cuadrilla).filter(Cuadrilla.nombre == "Cuadrilla E2E").first()
        id_cuadrilla = cuadrilla.id
    else:
        id_cuadrilla = int(current_entity["data"]["id"])
    print(id_cuadrilla)
    seleccion = update_selection(db_session, id_cuadrilla, s.id_obra, s.id_sucursal, current_entity)
    return {"id": seleccion.id, "id_cuadrilla": seleccion.id_cuadrilla, "id_obra": seleccion.id_obra, "id_sucursal": seleccion.id_sucursal}

@router.delete("/sucursal/{id_sucursal}", response_model=dict)
def sucursal_delete(request: Request, id_sucursal: int, db_session: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    if os.environ.get("E2E_TESTING") == "true":
        cuadrilla = db_session.query(Cuadrilla).filter(Cuadrilla.nombre == "Cuadrilla E2E").first()
        id_cuadrilla = cuadrilla.id
    else:
        id_cuadrilla = int(current_entity["data"]["id"])
    return delete_sucursal(db_session, id_cuadrilla, id_sucursal, current_entity)

@router.delete("/delete-obra/{id_obra}", response_model=dict)
def obra_delete(request: Request, id_obra: int, db_session: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    if os.environ.get("E2E_TESTING") == "true":
        cuadrilla = db_session.query(Cuadrilla).filter(Cuadrilla.nombre == "Cuadrilla E2E").first()
        id_cuadrilla = cuadrilla.id
    else:
        id_cuadrilla = int(current_entity["data"]["id"])
    return delete_obra(db_session, id_cuadrilla, id_obra, current_entity)

@router.delete("/selection", response_model=dict)
def selection_delete(request: Request, db_session: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    if os.environ.get("E2E_TESTING") == "true":
        cuadrilla = db_session.query(Cuadrilla).filter(Cuadrilla.nombre == "Cuadrilla E2E").first()
        id_cuadrilla = cuadrilla.id
    else:
        id_cuadrilla = int(current_entity["data"]["id"])
    return delete_selection(db_session, id_cuadrilla, current_entity)