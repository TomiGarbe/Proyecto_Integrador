import os

from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.models import Obra, FotoObra
from services.gcloud_storage import delete_file_in_folder
from services.google_sheets import update_correctivo

GOOGLE_CLOUD_BUCKET_NAME = os.getenv("GOOGLE_CLOUD_BUCKET_NAME")

def _ensure_entity(current_entity: dict):
    if not current_entity:
        raise HTTPException(status_code=401, detail="Autenticación requerida")

def _get_obra(db: Session, obra_id: int):
    obra = db.query(Obra).filter(Obra.id == obra_id).first()
    if not obra:
        raise HTTPException(status_code=404, detail="Obra no encontrada")
    return obra

def delete_obra_planilla(db: Session, obra_id: int, file_name: str, current_entity: dict) -> bool:
    _ensure_entity(current_entity)

    db_obra = _get_obra(db, obra_id)
    delete_file_in_folder(GOOGLE_CLOUD_BUCKET_NAME, f"obras/{obra_id}/planilla/", file_name)

    db_obra.planilla = None

    db.commit()
    db.refresh(db_obra)
    update_correctivo(db_obra)
    return True

def delete_obra_photo(db: Session, obra_id: int, file_name: str, current_entity: dict) -> bool:
    _ensure_entity(current_entity)

    db_obra = _get_obra(db, obra_id)

    foto = (
        db.query(FotoObra)
        .filter(
            FotoObra.obra_id == obra_id,
            FotoObra.url.endswith(file_name),
        )
        .first()
    )
    if not foto:
        raise HTTPException(status_code=404, detail="Foto no encontrada")

    delete_file_in_folder(GOOGLE_CLOUD_BUCKET_NAME, f"obras/{obra_id}/fotos/", file_name)
    db.delete(foto)
    db.commit()
    update_correctivo(db_obra)
    return True