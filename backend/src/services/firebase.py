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
