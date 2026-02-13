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

def _get_obra(db: Session, id_obra: int):
    obra = db.query(Obra).filter(Obra.id == id_obra).first()
    if not obra:
        raise HTTPException(status_code=404, detail="Obra no encontrada")
    return obra

def delete_planilla(db: Session, id_obra: int, file_name: str, current_entity: dict) -> bool:
    _ensure_entity(current_entity)

    db_obra = _get_obra(db, id_obra)
    delete_file_in_folder(GOOGLE_CLOUD_BUCKET_NAME, f"obras/{id_obra}/planilla/", file_name)

    db_obra.planilla = None

    db.commit()
    db.refresh(db_obra)
    update_correctivo(db_obra)
    return True

def delete_foto(db: Session, id_obra: int, file_name: str, current_entity: dict) -> bool:
    _ensure_entity(current_entity)

    db_obra = _get_obra(db, id_obra)

    foto = (
        db.query(FotoObra)
        .filter(
            FotoObra.id_obra == id_obra,
            FotoObra.url.endswith(file_name),
        )
        .first()
    )
    if not foto:
        raise HTTPException(status_code=404, detail="Foto no encontrada")

    delete_file_in_folder(GOOGLE_CLOUD_BUCKET_NAME, f"obras/{id_obra}/fotos/", file_name)
    db.delete(foto)
    db.commit()
    update_correctivo(db_obra)
    return True