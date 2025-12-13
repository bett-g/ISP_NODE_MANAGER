import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

# Simulamos credenciales de Admin (en producción esto iría en variables de entorno)
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Verifica usuario y contraseña, si falla, lanza un 401 y detiene la ejecución.
    """
    # Usamos compare_digest para evitar ataques de tiempo (Timing Attacks)
    is_user_correct = secrets.compare_digest(credentials.username, ADMIN_USER)
    is_pass_correct = secrets.compare_digest(credentials.password, ADMIN_PASS)

    if not (is_user_correct and is_pass_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    return credentials.username