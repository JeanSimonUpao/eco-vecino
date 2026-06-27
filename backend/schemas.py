"""
HU-001: Schemas Pydantic para autenticación y usuarios.
Valida los datos de entrada/salida del sistema de registro e inicio de sesión.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from backend.models import RolUsuario


# ── Registro ──────────────────────────────────────────────────────────────────

class UsuarioRegistro(BaseModel):
    """Datos requeridos para registrar un nuevo usuario."""
    nombre: str = Field(..., min_length=2, max_length=100, examples=["Juan Pérez"])
    email: EmailStr = Field(..., examples=["juan@municipio.pe"])
    password: str = Field(..., min_length=6, examples=["segura123"])
    rol: RolUsuario = Field(default=RolUsuario.vecino, examples=["vecino"])


# ── Login ─────────────────────────────────────────────────────────────────────

class UsuarioLogin(BaseModel):
    """Credenciales para iniciar sesión."""
    email: EmailStr = Field(..., examples=["juan@municipio.pe"])
    password: str = Field(..., examples=["segura123"])


# ── Respuestas ────────────────────────────────────────────────────────────────

class UsuarioRespuesta(BaseModel):
    """Datos públicos del usuario (sin contraseña)."""
    id: int
    nombre: str
    email: EmailStr
    rol: RolUsuario
    puntos_totales: int
    creado_en: Optional[datetime]

    model_config = {"from_attributes": True}


class TokenRespuesta(BaseModel):
    """Respuesta tras login exitoso."""
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioRespuesta


class MensajeRespuesta(BaseModel):
    """Respuesta genérica de mensaje."""
    mensaje: str
    detalle: Optional[str] = None
