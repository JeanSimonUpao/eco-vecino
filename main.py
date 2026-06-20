from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(title="Eco-Vecino API - CRUD Residuos y Mapas")

class Residuo(BaseModel):
    id: int
    tipo: str  # e.g., Plastico, Vidrio, Papel
    puntos_por_kg: int
    descripcion: Optional[str] = None

class CentroAcopio(BaseModel):
    id: int
    nombre: str
    direccion: str
    lat: float
    lng: float
    tipos_residuos: List[str]
    horario: str
    telefono: str

# Base de datos simulada en memoria
db_residuos: List[Residuo] = [
    Residuo(id=1, tipo="Plástico PET", puntos_por_kg=10, descripcion="Botellas de plástico transparentes"),
    Residuo(id=2, tipo="Vidrio", puntos_por_kg=5, descripcion="Botellas y frascos de vidrio"),
]

db_centros: List[CentroAcopio] = [
    CentroAcopio(
        id=1,
        nombre="Punto Ecológico Parque Central",
        direccion="Av. Larco 450, Miraflores",
        lat=-12.1218,
        lng=-77.0296,
        tipos_residuos=["Plástico", "Vidrio", "Papel"],
        horario="Lunes a Sábado: 8:00 AM - 6:00 PM",
        telefono="+51 987 654 321"
    ),
    CentroAcopio(
        id=2,
        nombre="Centro de Acopio San Isidro",
        direccion="Calle Los Libertadores 210, San Isidro",
        lat=-12.0984,
        lng=-77.0352,
        tipos_residuos=["Vidrio", "Metal"],
        horario="Lunes a Viernes: 9:00 AM - 5:00 PM",
        telefono="+51 912 345 678"
    ),
    CentroAcopio(
        id=3,
        nombre="Punto Verde Surco",
        direccion="Av. Caminos del Inca 1200, Santiago de Surco",
        lat=-12.1325,
        lng=-76.9845,
        tipos_residuos=["Plástico", "Papel", "Metal"],
        horario="Todos los días: 7:00 AM - 8:00 PM",
        telefono="+51 955 443 322"
    )
]

@app.get("/residuos", response_model=List[Residuo])
def listar_residuos():
    return db_residuos

@app.post("/residuos", response_model=Residuo)
def crear_residuo(residuo: Residuo):
    for r in db_residuos:
        if r.id == residuo.id:
            raise HTTPException(status_code=400, detail="El ID del residuo ya existe")
    db_residuos.append(residuo)
    return residuo

@app.delete("/residuos/{residuo_id}")
def eliminar_residuo(residuo_id: int):
    global db_residuos
    db_residuos = [r for r in db_residuos if r.id != residuo_id]
    return {"message": "Residuo eliminado exitosamente"}

@app.get("/api/centros", response_model=List[CentroAcopio])
def listar_centros():
    return db_centros

@app.get("/mapa", response_class=HTMLResponse)
def obtener_mapa():
    try:
        # Intentar ruta relativa al archivo actual
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates", "mapa.html")
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except Exception:
        # Fallback a ruta relativa simple
        with open("templates/mapa.html", "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)

