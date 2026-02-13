import os
from sqlalchemy import create_engine, Column, Integer, String
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

def init_db():
    """Inicializa la base de datos y crea las tablas."""
    Base.metadata.create_all(engine)
    
    # Crear el producto base si no existe
    session = SessionLocal()
    if not session.query(Producto).filter_by(nombre="Carton").first():
        nuevo_prod = Producto(nombre="Carton", cantidad=0)
        session.add(nuevo_prod)
        session.commit()
    session.close()