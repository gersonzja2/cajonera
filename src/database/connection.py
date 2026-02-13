import os
import bcrypt
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
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
    cantidad = Column(Integer, default=0)

class Movimiento(Base):
    __tablename__ = 'movimientos'

    id = Column(Integer, primary_key=True)
    fecha_hora = Column(DateTime, default=datetime.now)
    tipo_movimiento = Column(String, nullable=False) # 'entrada' o 'salida'
    cantidad = Column(Integer, nullable=False)
    usuario_id = Column(String, default="admin") # Guardamos el nombre del usuario (ej. 'admin')

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False) # 'admin' or 'vendedor'

def init_db():
    """Inicializa la base de datos y crea las tablas."""
    Base.metadata.create_all(engine)
    
    # Crear el producto base si no existe
    session = SessionLocal()
    if not session.query(Producto).filter_by(nombre="Carton").first():
        nuevo_prod = Producto(nombre="Carton", cantidad=0)
        session.add(nuevo_prod)
        session.commit()
    
    # Crear usuario admin por defecto si no existe
    if not session.query(Usuario).filter_by(username="admin").first():
        hashed = bcrypt.hashpw("admin".encode('utf-8'), bcrypt.gensalt())
        admin_user = Usuario(username="admin", password_hash=hashed.decode('utf-8'), role="admin")
        session.add(admin_user)
        session.commit()
    session.close()