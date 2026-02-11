from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from config.database import get_db
from services.obras import delete_obra_planilla, delete_obra_photo

router = APIRouter(prefix="/obras", tags=["obras"])

@router.delete("/{obra_id}/planilla/{file_name}", response_model=dict)
def mantenimiento_planilla_delete(obra_id: int, file_name: str, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    delete_mantenimiento_planilla(db, obra_id, file_name, current_entity)
    return {"message": "Planilla eliminada correctamente"}

@router.delete("/{obra_id}/fotos/{file_name}", response_model=dict)
def mantenimiento_photo_delete(obra_id: int, file_name: str, request: Request, db: Session = Depends(get_db)):
    current_entity = request.state.current_entity
    delete_mantenimiento_photo(db, obra_id, file_name, current_entity)
    return {"message": "Foto eliminada correctamente"}