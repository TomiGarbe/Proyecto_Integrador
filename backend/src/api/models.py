from sqlalchemy import Column, Integer, String, Date, ForeignKey, Text, DateTime, func, Boolean, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from datetime import datetime
from zoneinfo import ZoneInfo

Base = declarative_base()

class Zona(Base):
    __tablename__ = "zona"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)

class Cliente(Base):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    contacto = Column(String, nullable=False)
    email = Column(String, nullable=False)

    sucursales = relationship("Sucursal", back_populates="cliente", cascade="all, delete-orphan")
    mantenimientos_preventivos = relationship("MantenimientoPreventivo", back_populates="cliente")
    mantenimientos_correctivos = relationship("MantenimientoCorrectivo", back_populates="cliente")

class Sucursal(Base):
    __tablename__ = "sucursal"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    zona = Column(String)
    direccion = Column(String)
    superficie = Column(String)
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    frecuencia_preventivo = Column(String, nullable=True)
    
    cliente = relationship("Cliente", back_populates="sucursales")
    mantenimientos_preventivos = relationship("MantenimientoPreventivo", back_populates="sucursal")
    mantenimientos_correctivos = relationship("MantenimientoCorrectivo", back_populates="sucursal")
    asignaciones = relationship("ObraSeleccionada", back_populates="sucursal")

class Cuadrilla(Base):
    __tablename__ = "cuadrilla"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    zona = Column(String)
    email = Column(String, unique=True, nullable=False)
    firebase_uid = Column(String, unique=True, nullable=True)  # ID de Firebase
    
    mantenimientos_preventivos = relationship("MantenimientoPreventivo", back_populates="cuadrilla")
    mantenimientos_correctivos = relationship("MantenimientoCorrectivo", back_populates="cuadrilla")
    asignaciones = relationship("ObraSeleccionada", back_populates="cuadrilla")

class Obra(Base):
    __tablename__ = "obra"

    id = Column(Integer, primary_key=True)
    tipo = Column(String(20), nullable=False)

    mantenimiento_correctivo = relationship("MantenimientoCorrectivo", back_populates="obra", uselist=False)
    mantenimiento_preventivo = relationship("MantenimientoPreventivo", back_populates="obra", uselist=False)
    fotos = relationship("FotoObra", back_populates="obra", cascade="all, delete")
    mensajes = relationship("Mensaje", back_populates="obra", cascade="all, delete")
    notificaciones = relationship("Notificacion", back_populates="obra", cascade="all, delete")
    movimientos_stock = relationship("MovimientoStock", back_populates="obra")
    asignaciones = relationship("ObraSeleccionada", back_populates="obra")

class MantenimientoPreventivo(Base):
    __tablename__ = "mantenimiento_preventivo"
    id = Column(Integer, primary_key=True)
    obra_id = Column(Integer, ForeignKey("obra.id"), unique=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    id_sucursal = Column(Integer, ForeignKey("sucursal.id"), nullable=False)
    frecuencia = Column(String)
    id_cuadrilla = Column(Integer, ForeignKey("cuadrilla.id"))
    fecha_apertura = Column(Date)
    fecha_cierre = Column(Date, nullable=True)
    extendido = Column(DateTime, nullable=True)
    estado = Column(String)

    obra = relationship("Obra", back_populates="mantenimiento_preventivo")
    cliente = relationship("Cliente", back_populates="mantenimientos_preventivos")
    sucursal = relationship("Sucursal", back_populates="mantenimientos_preventivos")
    cuadrilla = relationship("Cuadrilla", back_populates="mantenimientos_preventivos")
    planillas = relationship("MantenimientoPreventivoPlanilla", backref="mantenimiento")
    
class MantenimientoPreventivoPlanilla(Base):
    __tablename__ = "mantenimiento_preventivo_planilla"
    id = Column(Integer, primary_key=True)
    mantenimiento_id = Column(Integer, ForeignKey("mantenimiento_preventivo.id"))
    url = Column(String, nullable=False)

class MantenimientoCorrectivo(Base):
    __tablename__ = "mantenimiento_correctivo"
    id = Column(Integer, primary_key=True)
    id_obra = Column(Integer, ForeignKey("obra.id"), unique=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id"), nullable=False)
    id_sucursal = Column(Integer, ForeignKey("sucursal.id"), nullable=False)
    id_cuadrilla = Column(Integer, ForeignKey("cuadrilla.id"))
    fecha_apertura = Column(Date)
    fecha_cierre = Column(Date, nullable=True)
    numero_caso = Column(String)
    incidente = Column(String)
    rubro = Column(String)
    planilla = Column(String)
    estado = Column(String)
    prioridad = Column(String)
    extendido = Column(DateTime, nullable=True)
    
    obra = relationship("Obra", back_populates="mantenimiento_correctivo")
    cliente = relationship("Cliente", back_populates="mantenimientos_correctivos")
    sucursal = relationship("Sucursal", back_populates="mantenimientos_correctivos")
    cuadrilla = relationship("Cuadrilla", back_populates="mantenimientos_correctivos")

class FotoObra(Base):
    __tablename__ = "foto_obra"
    id = Column(Integer, primary_key=True)
    id_obra = Column(Integer, ForeignKey("obra.id"))
    url = Column(String, nullable=False)

    obra = relationship("Obra", back_populates="fotos")

class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    email = Column(String, unique=True, nullable=False)
    rol = Column(String)
    firebase_uid = Column(String, unique=True, nullable=True)  # ID de Firebase

class ObraSeleccionada(Base):
    __tablename__ = "obra_seleccionada"
    id = Column(Integer, primary_key=True)
    id_cuadrilla = Column(Integer, ForeignKey("cuadrilla.id"))
    id_obra = Column(Integer, ForeignKey("obra.id"))
    id_sucursal = Column(Integer, ForeignKey("sucursal.id"))
    
    obra = relationship("Obra", back_populates="asignaciones")
    cuadrilla = relationship("Cuadrilla", back_populates="asignaciones")
    sucursal = relationship("Sucursal", back_populates="asignaciones")

class PushSubscription(Base):
    __tablename__ = "push_subscription"

    id = Column(Integer, primary_key=True, index=True)
    firebase_uid = Column(String, nullable=False)
    endpoint = Column(String, nullable=False)
    p256dh = Column(String, nullable=False)
    auth = Column(String, nullable=False)
    device_info = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
class Notificacion(Base):
    __tablename__ = "notificacion"

    id = Column(Integer, primary_key=True)
    firebase_uid = Column(String, nullable=False)
    id_obra = Column(Integer, ForeignKey("obra.id"))
    mensaje = Column(String, nullable=False)
    leida = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")))
    
    obra = relationship("Obra", back_populates="notificaciones")

class Mensaje(Base):
    __tablename__ = "mensaje"
    id = Column(Integer, primary_key=True)
    firebase_uid = Column(String)
    nombre_usuario = Column(String)
    id_obra = Column(Integer, ForeignKey("obra.id"))
    texto = Column(String, nullable=True)
    archivo = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")))

    obra = relationship("Obra", back_populates="mensajes")

class ColumnPreference(Base):
    __tablename__ = "column_preference"

    id = Column(Integer, primary_key=True)
    firebase_uid = Column(String, nullable=False, index=True)
    page = Column(String, nullable=False)
    columns = Column(Text, nullable=False)

class Material(Base):
    __tablename__ = "materiales"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    categoria = Column(String(100))
    unidad_medida = Column(String(20), nullable=False)
    descripcion = Column(Text)
    stock_actual = Column(Numeric(10,2), default=0)
    stock_minimo = Column(Numeric(10,2), default=0)

    movimientos = relationship("MovimientoStock", back_populates="material")

class MovimientoStock(Base):
    __tablename__ = "movimientos_stock"

    id = Column(Integer, primary_key=True, index=True)
    id_material = Column(Integer, ForeignKey("materiales.id"), nullable=False)
    tipo_movimiento = Column(String(20), nullable=False)
    cantidad = Column(Numeric(10,2), nullable=False)
    id_obra = Column(Integer, ForeignKey("obra.id"), nullable=True)
    fecha = Column(DateTime(timezone=True), default=lambda: datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")))

    obra = relationship("Obra", back_populates="movimientos_stock")
    material = relationship("Material", back_populates="movimientos")
