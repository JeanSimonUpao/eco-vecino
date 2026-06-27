"""
HU-004: Router para el historial de puntos del vecino.
Muestra fecha, tipo de residuo y puntos obtenidos por cada entrega.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from backend.database import get_db
from backend.models import TransaccionPuntos, EntregaResiduo, Usuario
from backend.routers.auth import get_current_user

router = APIRouter(prefix="/puntos", tags=["Puntos e Historial"])


# ── Schemas de respuesta ──────────────────────────────────────────────────────

class ItemHistorial(BaseModel):
    """Un registro del historial de puntos del usuario."""
    id: int
    fecha: datetime
    concepto: str
    puntos: int
    tipo_residuo: Optional[str] = None        # Nombre del residuo si aplica
    cantidad_kg: Optional[float] = None       # Kg entregados si aplica

    model_config = {"from_attributes": True}


class HistorialRespuesta(BaseModel):
    """Respuesta completa del historial de puntos."""
    usuario_id: int
    nombre: str
    puntos_totales: int
    total_entregas: int
    historial: List[ItemHistorial]


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get(
    "/historial",
    response_model=HistorialRespuesta,
    summary="Ver mi historial de puntos",
)
def ver_historial(
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    """
    Retorna el historial completo de puntos del usuario autenticado.

    Cada ítem incluye:
    - **fecha**: Cuándo se realizó la transacción
    - **concepto**: Descripción (ej. "Entrega de Plástico PET")
    - **puntos**: Puntos obtenidos (positivo) o canjeados (negativo)
    - **tipo_residuo**: Tipo de residuo entregado (si aplica)
    - **cantidad_kg**: Kilogramos entregados (si aplica)
    """
    # Obtener todas las transacciones del usuario ordenadas por fecha descendente
    transacciones = (
        db.query(TransaccionPuntos)
        .filter(TransaccionPuntos.usuario_id == usuario.id)
        .order_by(TransaccionPuntos.creado_en.desc())
        .all()
    )

    historial = []
    for t in transacciones:
        item = ItemHistorial(
            id=t.id,
            fecha=t.creado_en,
            concepto=t.concepto,
            puntos=t.puntos,
        )
        # Si la transacción está asociada a una entrega, enriquecer con detalles
        if t.entrega_id:
            entrega = db.query(EntregaResiduo).filter(
                EntregaResiduo.id == t.entrega_id
            ).first()
            if entrega and entrega.tipo_residuo:
                item.tipo_residuo = entrega.tipo_residuo.nombre
                item.cantidad_kg = entrega.cantidad_kg

        historial.append(item)

    total_entregas = (
        db.query(EntregaResiduo)
        .filter(EntregaResiduo.usuario_id == usuario.id)
        .count()
    )

    return HistorialRespuesta(
        usuario_id=usuario.id,
        nombre=usuario.nombre,
        puntos_totales=usuario.puntos_totales,
        total_entregas=total_entregas,
        historial=historial,
    )


@router.get(
    "/resumen",
    summary="Resumen rápido de mis puntos",
)
def resumen_puntos(usuario: Usuario = Depends(get_current_user)):
    """
    Retorna un resumen rápido de los puntos acumulados del usuario autenticado.
    """
    return {
        "usuario": usuario.nombre,
        "puntos_totales": usuario.puntos_totales,
        "mensaje": f"¡Llevas {usuario.puntos_totales} puntos ecológicos acumulados! 🌱",
    }
