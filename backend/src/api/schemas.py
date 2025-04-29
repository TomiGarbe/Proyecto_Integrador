from pydantic import BaseModel
from typing import Optional

# Esquemas para Zona
class Zona(BaseModel):
    nombre: str

# Esquemas para Sucursal
class SucursalCreate(BaseModel):
    nombre: str
    zona: str
    direccion: str
    superficie: str

class SucursalUpdate(BaseModel):
    nombre: Optional[str] = None
    zona: Optional[str] = None
    direccion: Optional[str] = None
    superficie: Optional[str] = None