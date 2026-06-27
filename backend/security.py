"""
SP-001: Módulo de seguridad y autenticación JWT.
Librería seleccionada: python-jose[cryptography] + passlib[bcrypt]
Decisión documentada en: docs/JWT_LIBRARY_COMPARISON.md
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv()

# ── Configuración desde variables de entorno ──────────────────────────────────
SECRET_KEY: str = os.getenv("SECRET_KEY", "clave_insegura_solo_para_dev")
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)

# ── Contexto de hash de contraseñas (bcrypt) ─────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str) -> str:
    """Genera el hash bcrypt de una contraseña en texto plano."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica que una contraseña en texto plano coincida con su hash."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Genera un JWT de acceso con los datos del usuario.

    Args:
        data: Payload del token (ej. {"sub": "user@email.com", "rol": "vecino"})
        expires_delta: Tiempo de expiración. Por defecto usa ACCESS_TOKEN_EXPIRE_MINUTES.

    Returns:
        Token JWT firmado como string.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodifica y valida un JWT.

    Returns:
        Payload del token si es válido, None si expiró o es inválido.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
