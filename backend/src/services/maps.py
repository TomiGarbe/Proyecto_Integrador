from fastapi import HTTPException   
from sqlalchemy.orm import Session
from api.models import ObraSeleccionada
from pydantic import BaseModel
from typing import List
from firebase_admin import db
from auth.firebase import initialize_firebase

class Sucursal(BaseModel):
    id: str
    name: str
    lat: float
    lng: float
    
class Usuarios(BaseModel):
    id: str
    tipo: str
    name: str
    lat: float
    lng: float

def _ensure_usuario(current_entity: dict):
    if not current_entity:
        raise HTTPException(status_code=401, detail="Autenticación requerida")
    if current_entity.get("type") != "usuario":
        raise HTTPException(status_code=403, detail="No tienes permisos")

def _ensure_entity(current_entity: dict):
    if not current_entity:
        raise HTTPException(status_code=401, detail="Autenticación requerida")

async def get_sucursales_locations(current_entity: dict) -> List[Sucursal]:
    _ensure_entity(current_entity)
    
    try:
        initialize_firebase()
        ref = db.reference('/sucursales')
        sucursales_data = ref.get()
        if sucursales_data is None:
            return []
        if isinstance(sucursales_data, list):
            return [
                Sucursal(id=str(i), name=data.get('name', 'Unknown'), lat=data.get('lat', 0.0), lng=data.get('lng', 0.0))
                for i, data in enumerate(sucursales_data) if data is not None
            ]
        return [
            Sucursal(id=id_sucursal, name=data.get('name', 'Unknown'), lat=data.get('lat', 0.0), lng=data.get('lng', 0.0))
            for id_sucursal, data in sucursales_data.items()
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo sucursales de Firebase: {str(e)}")

async def get_users_locations(current_entity: dict) -> List[Usuarios]:
    _ensure_usuario(current_entity)
    
    try:
        initialize_firebase()
        ref = db.reference('/users')
        users_data = ref.get()

        if not users_data:
            return []

        return [
            Usuarios(
                id=data.get("id"),
                tipo=data.get("tipo"),
                name=data.get("name", "Unknown"),
                lat=data.get("lat", 0.0),
                lng=data.get("lng", 0.0)
            )
            for data in users_data.values()
            if data
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")
    
def get_selection(db_session: Session, id_cuadrilla: int, current_entity: dict):
    _ensure_entity(current_entity)

    obras = db_session.query(ObraSeleccionada).filter(ObraSeleccionada.id_cuadrilla == id_cuadrilla).all()
    if not obras:
        return []
    return obras

async def update_user_location(current_entity: dict, firebase_uid: str, id_user: str, tipo: str, name: str, lat: float, lng: float):
    _ensure_entity(current_entity)
    
    try:
        initialize_firebase()
        ref = db.reference(f'/users/{firebase_uid}')
        ref.set({
            'id': id_user,
            'tipo': tipo,
            'name': name,
            'lat': lat,
            'lng': lng
        })
        return {"message": f"Ubicación actualizada para {id_user}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error actualizando ubicación: {str(e)}")

def update_selection(db_session: Session, id_cuadrilla: int, id_obra: int, id_sucursal: int, current_entity: dict):
    _ensure_entity(current_entity)
    
    existing_obra = db_session.query(ObraSeleccionada).filter(
        ObraSeleccionada.id_cuadrilla == id_cuadrilla,
        ObraSeleccionada.id_obra == id_obra
    ).first()

    if existing_obra:
        raise HTTPException(status_code=400, detail="La obra ya fue seleccionada anteriormente")
    
    try:
        db_obra = ObraSeleccionada(id_cuadrilla=id_cuadrilla, id_obra=id_obra, id_sucursal=id_sucursal)
        db_session.add(db_obra)
        db_session.commit()
        db_session.refresh(db_obra)
        return db_obra
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al guardar obra: {str(e)}")
    
def delete_sucursal(db_session: Session, id_cuadrilla: int, id_sucursal: int, current_entity: dict):
    _ensure_entity(current_entity)
    
    obras = db_session.query(ObraSeleccionada).filter(
        ObraSeleccionada.id_cuadrilla == id_cuadrilla,
        ObraSeleccionada.id_sucursal == id_sucursal
    ).all()
    if obras:
        for obra in obras:
            db_session.delete(obra)

    db_session.commit()
    return {"message": "Seleccion de sucursal eliminada"}

def delete_obra(db_session: Session, id_cuadrilla: int, id_obra: int, current_entity: dict):
    _ensure_entity(current_entity)
    
    obra = db_session.query(ObraSeleccionada).filter(
        ObraSeleccionada.id_cuadrilla == id_cuadrilla,
        ObraSeleccionada.id_obra == id_obra
    ).first()
    if not obra:
        raise HTTPException(status_code=404, detail="Obra no encontrada")
        
    db_session.delete(obra)
    db_session.commit()
    return {"message": "Seleccion de obra eliminada"}

def delete_selection(db_session: Session, id_cuadrilla: int, current_entity: dict):
    _ensure_entity(current_entity)
        
    obras = db_session.query(ObraSeleccionada).filter(ObraSeleccionada.id_cuadrilla == id_cuadrilla).all()
    if obras:
        for obra in obras:
            db_session.delete(obra)

    db_session.commit()
    return {"message": "Seleccion eliminada"}