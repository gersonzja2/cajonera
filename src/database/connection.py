import os
import shutil
import bcrypt
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la Base de Datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/cajonera.db")

Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

class Producto(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    codigo = Column(String, unique=True, nullable=True) # SKU o Código de Barras
    categoria = Column(String, default="General")
    precio_costo = Column(Float, default=0.0)
    precio_venta = Column(Float, default=0.0)
    stock_minimo = Column(Integer, default=10) # Punto de Reorden
    activo = Column(Boolean, default=True) # Para borrado lógico
    cantidad = Column(Integer, default=0)

class Movimiento(Base):
    __tablename__ = 'movimientos'

    id = Column(Integer, primary_key=True)
    fecha_hora = Column(DateTime, default=datetime.now)
    producto_id = Column(Integer, ForeignKey('productos.id')) # Vinculamos con el ID del producto
    tipo_movimiento = Column(String, nullable=False) # 'entrada' o 'salida'
    cantidad = Column(Integer, nullable=False)
    usuario_id = Column(String, default="admin") # Guardamos el nombre del usuario (ej. 'admin')

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    telefono = Column(String, nullable=True)
    email = Column(String, nullable=True)

class Venta(Base):
    __tablename__ = 'ventas'

    id = Column(Integer, primary_key=True)
    fecha_hora = Column(DateTime, default=datetime.now)
    producto_id = Column(Integer, ForeignKey('productos.id'))
    cliente_id = Column(Integer, ForeignKey('clientes.id'), nullable=True) # Puede ser nulo (Consumidor Final)
    cantidad = Column(Integer, nullable=False)
    total = Column(Float, nullable=False) # Precio Venta * Cantidad
    ganancia = Column(Float, default=0.0) # (Precio Venta - Precio Costo) * Cantidad
    usuario_id = Column(String, default="admin")
    reembolsado = Column(Boolean, default=False) # Para marcar si ya fue devuelta

class Proveedor(Base):
    __tablename__ = 'proveedores'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, unique=True, nullable=False)
    contacto = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    email = Column(String, nullable=True)

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False) # 'admin' or 'vendedor'

def init_db():
    """Inicializa la base de datos y crea las tablas."""
    Base.metadata.create_all(engine)
    
    session = SessionLocal()
    
    # Crear usuario admin por defecto si no existe
    if not session.query(Usuario).filter_by(username="admin").first():
        hashed = bcrypt.hashpw("admin".encode('utf-8'), bcrypt.gensalt())
        admin_user = Usuario(username="admin", password_hash=hashed.decode('utf-8'), role="admin")
        session.add(admin_user)
        session.commit()
    session.close()

def backup_db():
    """Crea una copia de seguridad de la base de datos al cerrar."""
    if not os.path.exists("backups"):
        os.makedirs("backups")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    db_path = "data/cajonera.db"
    if os.path.exists(db_path):
        backup_path = f"backups/cajonera_backup_{timestamp}.db"
        shutil.copy2(db_path, backup_path)