"""
EN-001: Modelos ORM iniciales para Eco-Vecino
Define las tablas base del sistema usando SQLAlchemy.
"""

from sqlalchemy import (
    Column, Integer, String, Float, Text,
    DateTime, ForeignKey, Enum as SAEnum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from backend.database import Base


class RolUsuario(str, enum.Enum):
    """Roles disponibles en la plataforma."""
    vecino = "vecino"
    administrador = "administrador"
    operador = "operador"


class Usuario(Base):
    """
    Tabla de usuarios del sistema.
    Soporta 4 tipos de usuario según HU-001.
    """
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    rol = Column(SAEnum(RolUsuario), default=RolUsuario.vecino, nullable=False)
    puntos_totales = Column(Integer, default=0, nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    entregas = relationship("EntregaResiduo", back_populates="usuario")
    transacciones_puntos = relationship("TransaccionPuntos", back_populates="usuario")

    def __repr__(self):
        return f"<Usuario id={self.id} email={self.email} rol={self.rol}>"


class TipoResiduo(Base):
    """
    Catálogo de tipos de residuos reciclables con su valor en puntos.
    """
    __tablename__ = "tipos_residuo"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)   # ej: Plástico PET
    puntos_por_kg = Column(Float, nullable=False, default=0.0)
    descripcion = Column(Text, nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    entregas = relationship("EntregaResiduo", back_populates="tipo_residuo")

    def __repr__(self):
        return f"<TipoResiduo {self.nombre} ({self.puntos_por_kg} pts/kg)>"


class CentroAcopio(Base):
    """
    Centros de acopio donde los vecinos entregan sus residuos.
    """
    __tablename__ = "centros_acopio"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    direccion = Column(String(300), nullable=False)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    horario = Column(String(200), nullable=True)
    telefono = Column(String(20), nullable=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    entregas = relationship("EntregaResiduo", back_populates="centro")

    def __repr__(self):
        return f"<CentroAcopio {self.nombre}>"


class EntregaResiduo(Base):
    """
    Registro de cada entrega de residuos realizada por un vecino.
    Tabla central del sistema de puntos.
    """
    __tablename__ = "entregas_residuo"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo_residuo_id = Column(Integer, ForeignKey("tipos_residuo.id"), nullable=False)
    centro_id = Column(Integer, ForeignKey("centros_acopio.id"), nullable=False)
    cantidad_kg = Column(Float, nullable=False)
    puntos_obtenidos = Column(Integer, nullable=False, default=0)
    codigo_qr = Column(String(255), unique=True, nullable=True)  # Para HU-006
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    usuario = relationship("Usuario", back_populates="entregas")
    tipo_residuo = relationship("TipoResiduo", back_populates="entregas")
    centro = relationship("CentroAcopio", back_populates="entregas")

    def __repr__(self):
        return f"<EntregaResiduo usuario={self.usuario_id} puntos={self.puntos_obtenidos}>"


class TransaccionPuntos(Base):
    """
    Historial de transacciones de puntos por usuario (RN-001).
    Registro inmutable para garantizar integridad del sistema de gamificación.
    """
    __tablename__ = "transacciones_puntos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    entrega_id = Column(Integer, ForeignKey("entregas_residuo.id"), nullable=True)
    puntos = Column(Integer, nullable=False)            # positivo = ganado, negativo = canje
    concepto = Column(String(300), nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    usuario = relationship("Usuario", back_populates="transacciones_puntos")

    def __repr__(self):
        return f"<TransaccionPuntos usuario={self.usuario_id} puntos={self.puntos}>"
