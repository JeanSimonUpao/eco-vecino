"""
SP-002: Router de centros de acopio — integración con API de mapas.
Expone los datos de centros de acopio para consumo desde el mapa interactivo.
API seleccionada: Leaflet + OpenStreetMap/CartoDB (ver docs/MAP_API_COMPARISON.md)
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from backend.database import get_db
from backend.models import CentroAcopio

router = APIRouter(prefix="/centros", tags=["Centros de Acopio"])


# ── Schemas ───────────────────────────────────────────────────────────────────

class CentroAcopioRespuesta(BaseModel):
    """Datos de un centro de acopio para mostrar en el mapa."""
    id: int
    nombre: str
    direccion: str
    latitud: float
    longitud: float
    horario: Optional[str]
    telefono: Optional[str]

    model_config = {"from_attributes": True}


class CentroAcopioCrear(BaseModel):
    """Datos para registrar un nuevo centro de acopio."""
    nombre: str
    direccion: str
    latitud: float
    longitud: float
    horario: Optional[str] = None
    telefono: Optional[str] = None


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get(
    "/",
    response_model=List[CentroAcopioRespuesta],
    summary="Listar todos los centros de acopio",
)
def listar_centros(db: Session = Depends(get_db)):
    """
    Retorna todos los centros de acopio registrados.
    Este endpoint es consumido por el mapa interactivo (Leaflet + OSM).
    No requiere autenticación — es información pública.
    """
    return db.query(CentroAcopio).all()


@router.get(
    "/{centro_id}",
    response_model=CentroAcopioRespuesta,
    summary="Obtener un centro de acopio por ID",
)
def obtener_centro(centro_id: int, db: Session = Depends(get_db)):
    """Retorna los datos de un centro de acopio específico."""
    centro = db.query(CentroAcopio).filter(CentroAcopio.id == centro_id).first()
    if not centro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Centro de acopio con ID {centro_id} no encontrado",
        )
    return centro


@router.post(
    "/",
    response_model=CentroAcopioRespuesta,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo centro de acopio",
)
def crear_centro(datos: CentroAcopioCrear, db: Session = Depends(get_db)):
    """
    Registra un nuevo centro de acopio en la base de datos.
    Los datos de latitud/longitud son usados por Leaflet para posicionar el marcador.
    """
    nuevo = CentroAcopio(
        nombre=datos.nombre,
        direccion=datos.direccion,
        latitud=datos.latitud,
        longitud=datos.longitud,
        horario=datos.horario,
        telefono=datos.telefono,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


@router.get(
    "/mapa/datos",
    summary="Datos optimizados para el mapa interactivo",
)
def datos_para_mapa(db: Session = Depends(get_db)):
    """
    Retorna los centros en formato GeoJSON-compatible para Leaflet.
    Incluye solo lat/lng/nombre para minimizar el payload del mapa.
    """
    centros = db.query(CentroAcopio).all()
    return {
        "tipo": "FeatureCollection",
        "total": len(centros),
        "api_mapa": "Leaflet + CartoDB Voyager (ver docs/MAP_API_COMPARISON.md)",
        "features": [
            {
                "id": c.id,
                "nombre": c.nombre,
                "lat": c.latitud,
                "lng": c.longitud,
                "popup": f"<b>{c.nombre}</b><br>{c.direccion}<br>{c.horario or ''}",
            }
            for c in centros
        ],
    }
