from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from config.database import get_db
from services.obras import delete_planilla, delete_foto

router = APIRouter(prefix="/obras", tags=["obras"])

@router.delete("/{id_obra}/planilla/{file_name}", response_model=dict)
def planilla_delete(id_obra: int, file_name: str, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    delete_planilla(db, id_obra, file_name, current_entity)
    return {"message": "Planilla eliminada correctamente"}

@router.delete("/{id_obra}/fotos/{file_name}", response_model=dict)
def foto_delete(id_obra: int, file_name: str, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    delete_foto(db, id_obra, file_name, current_entity)
    return {"message": "Foto eliminada correctamente"}