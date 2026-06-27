"""
EN-001: Script de inicialización de base de datos.
Crea todas las tablas definidas en los modelos ORM.
"""

from backend.database import engine, Base
from backend import models  # noqa: F401 - importar para registrar todos los modelos


def init_db():
    """Crea todas las tablas en PostgreSQL si no existen."""
    print("🔄 Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tablas creadas exitosamente:")
    for table_name in Base.metadata.tables.keys():
        print(f"   - {table_name}")


if __name__ == "__main__":
    init_db()
