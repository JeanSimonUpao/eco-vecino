"""
Eco-Vecino API — Punto de entrada principal.
Integra todos los routers del sistema.
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

from backend.routers.auth import router as auth_router
from backend.routers.puntos import router as puntos_router
from backend.routers.centros import router as centros_router  # SP-002

app = FastAPI(
    title="Eco-Vecino API",
    description="Plataforma de gestión de residuos reciclables y puntos ecológicos municipales",
    version="0.1.0",
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(puntos_router)  # HU-004
app.include_router(centros_router)  # SP-002 / HU-005

# ── Rutas legacy (pendientes de migrar) ──────────────────────────────────────

@app.get("/mapa", response_class=HTMLResponse, tags=["Mapa"])
def obtener_mapa():
    """Sirve la interfaz del mapa de centros de acopio."""
    try:
        filepath = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "templates", "mapa.html"
        )
        with open(filepath, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception:
        with open("templates/mapa.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())


@app.get("/", tags=["Root"])
def root():
    return {
        "proyecto": "Eco-Vecino",
        "version": "0.1.0",
        "docs": "/docs",
    }
