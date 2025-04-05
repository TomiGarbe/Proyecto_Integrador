# Crear estructura de directorios
New-Item -ItemType Directory -Force -Path "backend/src/api", "backend/src/services", "backend/src/config", "backend/tests"
New-Item -ItemType Directory -Force -Path "frontend/public", "frontend/src/components", "frontend/src/pages", "frontend/src/services", "frontend/tests", "frontend/cypress/integration"
New-Item -ItemType Directory -Force -Path ".github/workflows"

# Archivos del backend
Set-Content -Path "backend/src/api/__init__.py" -Value "# Módulo vacío"

Set-Content -Path "backend/src/api/routes.py" -Value @"
# Ejemplo con FastAPI (ajusta según tu framework)
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
"@

Set-Content -Path "backend/src/api/models.py" -Value @"
# Modelos para SQLAlchemy (ejemplo básico)
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
"@

Set-Content -Path "backend/src/services/__init__.py" -Value "# Módulo vacío"

Set-Content -Path "backend/src/services/google_sheets.py" -Value @"
# Ejemplo de integración con Google Sheets
def sync_to_sheets(data):
    # Lógica para sincronizar con Google Sheets
    pass
"@

Set-Content -Path "backend/src/services/firebase.py" -Value @"
# Ejemplo de integración con Firebase
import pyrebase

def init_firebase():
    config = {
        "apiKey": "your-api-key",
        "authDomain": "your-app.firebaseapp.com",
        "databaseURL": "https://your-app.firebaseio.com",
        "projectId": "your-app",
    }
    return pyrebase.initialize_app(config)
"@

Set-Content -Path "backend/src/services/google_maps.py" -Value @"
# Ejemplo de integración con Google Maps API
def get_route(start, end):
    # Lógica para calcular rutas
    pass
"@

Set-Content -Path "backend/src/config/__init__.py" -Value "# Módulo vacío"

Set-Content -Path "backend/src/config/database.py" -Value @"
# Configuración de PostgreSQL con SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user:password@localhost:5432/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"@

Set-Content -Path "backend/src/main.py" -Value @"
from api.routes import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
"@

Set-Content -Path "backend/tests/__init__.py" -Value "# Módulo vacío"

Set-Content -Path "backend/tests/test_api.py" -Value @"
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}
"@

Set-Content -Path "backend/tests/test_services.py" -Value @"
def test_dummy_service():
    assert True  # Placeholder para pruebas de servicios
"@

Set-Content -Path "backend/requirements.txt" -Value @"
fastapi==0.95.0
uvicorn==0.21.1
sqlalchemy==2.0.0
psycopg2-binary==2.9.6
pyrebase4==4.6.0
google-auth==2.17.0
google-api-python-client==2.86.0
pytest==7.3.1
"@

Set-Content -Path "backend/.env" -Value @"
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
FIREBASE_API_KEY=your_firebase_api_key
GOOGLE_SHEETS_CREDENTIALS=your_credentials_json
GOOGLE_CLOUD_STORAGE_BUCKET=your_bucket_name
"@

# Archivos del frontend
Set-Content -Path "frontend/public/index.html" -Value @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Proyecto</title>
</head>
<body>
    <div id="root"></div>
</body>
</html>
"@

New-Item -ItemType File -Path "frontend/public/favicon.ico"

Set-Content -Path "frontend/src/components/Header.js" -Value @"
import React from 'react';

const Header = () => {
    return <header><h1>Gestión de Cuadrillas</h1></header>;
};

export default Header;
"@

Set-Content -Path "frontend/src/pages/Login.js" -Value @"
import React from 'react';

const Login = () => {
    return <div><h2>Iniciar Sesión</h2></div>;
};

export default Login;
"@

Set-Content -Path "frontend/src/pages/Dashboard.js" -Value @"
import React from 'react';

const Dashboard = () => {
    return <div><h2>Dashboard</h2></div>;
};

export default Dashboard;
"@

Set-Content -Path "frontend/src/pages/CrewManagement.js" -Value @"
import React from 'react';

const CrewManagement = () => {
    return <div><h2>Gestión de Cuadrillas</h2></div>;
};

export default CrewManagement;
"@

Set-Content -Path "frontend/src/services/api.js" -Value @"
import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8000',
});

export default api;
"@

Set-Content -Path "frontend/src/services/firebase.js" -Value @"
import firebase from "firebase/app";
import "firebase/auth";
import "firebase/database";

const firebaseConfig = {
    apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
    authDomain: "your-app.firebaseapp.com",
    databaseURL: "https://your-app.firebaseio.com",
    projectId: "your-app",
};

firebase.initializeApp(firebaseConfig);
export const auth = firebase.auth();
export const db = firebase.database();
"@

Set-Content -Path "frontend/src/App.js" -Value @"
import React from 'react';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';

function App() {
    return (
        <div>
            <Header />
            <Dashboard />
        </div>
    );
}

export default App;
"@

Set-Content -Path "frontend/src/index.js" -Value @"
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

ReactDOM.render(<App />, document.getElementById('root'));
"@

Set-Content -Path "frontend/src/setupTests.js" -Value @"
// Configuración inicial para Jest
import '@testing-library/jest-dom';
"@

Set-Content -Path "frontend/tests/Header.test.js" -Value @"
import { render, screen } from '@testing-library/react';
import Header from '../src/components/Header';

test('renders header title', () => {
    render(<Header />);
    expect(screen.getByText('Gestión de Cuadrillas')).toBeInTheDocument();
});
"@

Set-Content -Path "frontend/tests/Dashboard.test.js" -Value @"
import { render, screen } from '@testing-library/react';
import Dashboard from '../src/pages/Dashboard';

test('renders dashboard', () => {
    render(<Dashboard />);
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
});
"@

Set-Content -Path "frontend/cypress/integration/login.spec.js" -Value @"
describe('Login Page', () => {
    it('should display login title', () => {
        cy.visit('/login');
        cy.contains('Iniciar Sesión');
    });
});
"@

Set-Content -Path "frontend/package.json" -Value @"
{
    "name": "mi-proyecto-frontend",
    "version": "0.1.0",
    "dependencies": {
        "react": "^18.2.0",
        "react-dom": "^18.2.0",
        "firebase": "^9.19.1",
        "axios": "^1.3.5"
    },
    "devDependencies": {
        "@testing-library/react": "^14.0.0",
        "jest": "^29.5.0",
        "cypress": "^12.9.0"
    },
    "scripts": {
        "start": "react-scripts start",
        "test": "jest",
        "cypress": "cypress open"
    }
}
"@

Set-Content -Path "frontend/.env" -Value @"
REACT_APP_FIREBASE_API_KEY=your_firebase_api_key
"@

# Pipeline
Set-Content -Path ".github/workflows/pipeline.yml" -Value @"
name: PIPELINE
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest
  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: "18"
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Run tests
        run: |
          cd frontend
          npm test
"@

# Otros archivos
Set-Content -Path ".gitignore" -Value @"
node_modules/
*.env
__pycache__/
*.pyc
.DS_Store
"@

Set-Content -Path "README.md" -Value @"
# Mi Proyecto
Sistema de gestión de cuadrillas para obras de mantenimiento.

## Tecnologías
- Backend: Python (FastAPI)
- Frontend: React
- Bases de datos: PostgreSQL, Firebase
- CI/CD: GitHub Actions
- Despliegue: Heroku

## Instalación
1. Clona el repositorio: `git clone <url>`
2. Configura las variables de entorno en `backend/.env` y `frontend/.env`.
3. Backend: `cd backend && pip install -r requirements.txt && python src/main.py`
4. Frontend: `cd frontend && npm install && npm start`
"@

Set-Content -Path "docker-compose.yml" -Value @"
version: "3.8"
services:
  db:
    image: postgres:14
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: dbname
    ports:
      - "5432:5432"
"@

Write-Host "¡Estructura del proyecto creada con éxito!"