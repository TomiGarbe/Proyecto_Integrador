from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import sucursales, zonas
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv(dotenv_path="./env.config")
FRONTEND_URL = os.getenv("FRONTEND_URL")

# Configuración de CORS
origins = [
    FRONTEND_URL,  # Origen del frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir solicitudes desde estos orígenes
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)


app.include_router(sucursales.router)
app.include_router(zonas.router)