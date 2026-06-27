"""
HU-001: Router de autenticación — Registro e inicio de sesión.
Implementa los endpoints para los 4 tipos de usuario del sistema Eco-Vecino.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas import (
    UsuarioRegistro,
    UsuarioRespuesta,
    TokenRespuesta,
    MensajeRespuesta,
)
from backend.crud_usuarios import (
    obtener_usuario_por_email,
    obtener_usuario_por_id,
    crear_usuario,
    autenticar_usuario,
)
from backend.security import create_access_token, decode_access_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

# Esquema OAuth2 — el token se obtiene en /auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ── Dependencia: usuario actual ───────────────────────────────────────────────

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Dependencia FastAPI que extrae y valida el usuario del JWT.
    Lanza 401 si el token es inválido o el usuario no existe.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas o token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    email: str = payload.get("sub")
    if not email:
        raise credentials_exception

    usuario = obtener_usuario_por_email(db, email)
    if usuario is None:
        raise credentials_exception

    return usuario


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post(
    "/registro",
    response_model=MensajeRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
)
def registrar_usuario(datos: UsuarioRegistro, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario en la plataforma.

    - **nombre**: Nombre completo del usuario
    - **email**: Correo electrónico único
    - **password**: Contraseña (mínimo 6 caracteres)
    - **rol**: vecino | administrador | operador (por defecto: vecino)

    Retorna error 400 si el email ya está registrado.
    """
    if obtener_usuario_por_email(db, datos.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado en el sistema",
        )
    crear_usuario(db, datos)
    return MensajeRespuesta(
        mensaje="Usuario registrado exitosamente",
        detalle=f"Bienvenido {datos.nombre}, ya puedes iniciar sesión",
    )


@router.post(
    "/login",
    response_model=TokenRespuesta,
    summary="Iniciar sesión",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Autentica al usuario y retorna un JWT de acceso.

    Usa el formato estándar OAuth2 (form-data):
    - **username**: Email del usuario
    - **password**: Contraseña

    Retorna error 401 si las credenciales son inválidas.
    """
    usuario = autenticar_usuario(db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(
        data={"sub": usuario.email, "rol": usuario.rol.value}
    )
    return TokenRespuesta(
        access_token=token,
        token_type="bearer",
        usuario=UsuarioRespuesta.model_validate(usuario),
    )


@router.get(
    "/me",
    response_model=UsuarioRespuesta,
    summary="Ver mi perfil (usuario autenticado)",
)
def ver_mi_perfil(usuario=Depends(get_current_user)):
    """
    Retorna los datos del usuario actualmente autenticado.
    Requiere token JWT en el header Authorization: Bearer <token>.
    """
    return UsuarioRespuesta.model_validate(usuario)
