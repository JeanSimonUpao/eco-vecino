from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Eco-Vecino API - CRUD Residuos")

class Residuo(BaseModel):
    id: int
    tipo: str  # e.g., Plastico, Vidrio, Papel
    puntos_por_kg: int
    descripcion: Optional[str] = None

# Base de datos simulada en memoria
db_residuos: List[Residuo] = [
    Residuo(id=1, tipo="Plástico PET", puntos_por_kg=10, descripcion="Botellas de plástico transparentes"),
    Residuo(id=2, tipo="Vidrio", puntos_por_kg=5, descripcion="Botellas y frascos de vidrio"),
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
