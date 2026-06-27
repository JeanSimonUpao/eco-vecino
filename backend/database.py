"""
EN-001: Configuración de la base de datos y ORM
Módulo principal de conexión a PostgreSQL usando SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# URL de conexión a PostgreSQL desde variable de entorno
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/eco_vecino"
)

# Motor de base de datos
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,          # Verifica conexiones antes de usarlas
    pool_size=10,                # Número de conexiones en el pool
    max_overflow=20,             # Conexiones extra permitidas sobre pool_size
    echo=False,                  # True para ver SQL generado en consola (debug)
)

# Fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base declarativa para todos los modelos ORM
Base = declarative_base()


def get_db():
    """
    Dependencia de FastAPI para inyectar sesión de DB en cada request.
    Garantiza que la sesión se cierre al finalizar el request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
