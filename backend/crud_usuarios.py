"""
HU-001: CRUD de usuarios en la base de datos.
Funciones de acceso a datos para registro, búsqueda y autenticación.
"""

from sqlalchemy.orm import Session
from typing import Optional

from backend.models import Usuario, RolUsuario
from backend.schemas import UsuarioRegistro
from backend.security import hash_password, verify_password


def obtener_usuario_por_email(db: Session, email: str) -> Optional[Usuario]:
    """Busca un usuario por su email. Retorna None si no existe."""
    return db.query(Usuario).filter(Usuario.email == email).first()


def obtener_usuario_por_id(db: Session, usuario_id: int) -> Optional[Usuario]:
    """Busca un usuario por su ID."""
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()


def crear_usuario(db: Session, datos: UsuarioRegistro) -> Usuario:
    """
    Registra un nuevo usuario en la base de datos.
    La contraseña se almacena como hash bcrypt, nunca en texto plano.
    """
    nuevo_usuario = Usuario(
        nombre=datos.nombre,
        email=datos.email,
        hashed_password=hash_password(datos.password),
        rol=datos.rol,
        puntos_totales=0,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


def autenticar_usuario(
    db: Session, email: str, password: str
) -> Optional[Usuario]:
    """
    Verifica credenciales de usuario.

    Returns:
        El objeto Usuario si las credenciales son válidas, None en caso contrario.
    """
    usuario = obtener_usuario_por_email(db, email)
    if not usuario:
        return None
    if not verify_password(password, usuario.hashed_password):
        return None
    return usuario
