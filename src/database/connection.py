import os
import shutil
import bcrypt
import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Configuración de Rutas (User Data) ---
# Usamos la carpeta de Documentos del usuario para garantizar permisos de escritura
USER_DIR = os.path.join(os.path.expanduser("~"), "Documents", "Cajonera")
DATA_DIR = os.path.join(USER_DIR, "data")
BACKUP_DIR = os.path.join(USER_DIR, "backups")
PDF_DIR = os.path.join(USER_DIR, "pdf")
CSV_DIR = os.path.join(USER_DIR, "csv")
LOG_FILE = os.path.join(USER_DIR, "error.log")

for d in [USER_DIR, DATA_DIR, BACKUP_DIR, PDF_DIR, CSV_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)

# Configuración de la Base de Datos
# Aseguramos que la ruta absoluta use barras normales para evitar problemas con SQLAlchemy en Windows
db_path_abs = os.path.join(DATA_DIR, 'cajonera.db')
# Forzamos el uso de la ruta en Documentos para evitar que .env o rutas relativas desvíen el archivo
DATABASE_URL = f"sqlite:///{db_path_abs.replace(os.sep, '/')}"

Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

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

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True)
    fecha_hora = Column(DateTime, default=datetime.now)
    usuario = Column(String, nullable=False)
    accion = Column(String, nullable=False)
    detalles = Column(String, nullable=True)

def setup_logging():
    """Configura el sistema de logging para guardar errores en archivo."""
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def init_db():
    """Inicializa la base de datos y crea las tablas."""
    # --- MIGRACIÓN AUTOMÁTICA ---
    # Si existe una base de datos antigua en la carpeta del proyecto, la copiamos a Documentos
    local_db = os.path.join(os.getcwd(), "data", "cajonera.db")
    target_db = os.path.join(DATA_DIR, "cajonera.db")
    
    if os.path.exists(local_db) and not os.path.exists(target_db):
        print(f"Detectada base de datos local. Migrando a: {target_db}")
        try:
            shutil.copy2(local_db, target_db)
            print("Migración completada exitosamente.")
        except Exception as e:
            print(f"Error al migrar base de datos: {e}")

    Base.metadata.create_all(engine)
    
    session = SessionLocal()
    
    # Crear usuario admin por defecto si no existe
    if not session.query(Usuario).filter_by(username="admin").first():
        hashed = bcrypt.hashpw("admin".encode('utf-8'), bcrypt.gensalt())
        admin_user = Usuario(username="admin", password_hash=hashed.decode('utf-8'), role="admin")
        session.add(admin_user)
        session.commit()
    
    # Detectar ruta real usada por SQLAlchemy
    db_path = engine.url.database
    if db_path and not os.path.isabs(db_path):
        db_path = os.path.abspath(db_path)

    print(f"Base de datos conectada en: {db_path}")
    if db_path and not os.path.exists(db_path):
        print("ADVERTENCIA: El archivo de base de datos no aparece en disco. Verifique permisos o ruta.")
    session.close()

def backup_db():
    """Crea una copia de seguridad de la base de datos al cerrar."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Usamos la ruta real del engine para asegurar que copiamos el archivo correcto
    db_path = engine.url.database
    if db_path and not os.path.isabs(db_path):
        db_path = os.path.abspath(db_path)

    if db_path and os.path.exists(db_path):
        try:
            backup_path = os.path.join(BACKUP_DIR, f"cajonera_backup_{timestamp}.db")
            shutil.copy2(db_path, backup_path)
            print(f"\n[BACKUP] Copia guardada exitosamente.")
            print(f" -> Ubicación: {backup_path}")
        except Exception as e:
            print(f"\n[BACKUP ERROR] No se pudo crear la copia: {e}")
    else:
        print(f"\n[BACKUP ERROR] No se encontró la base de datos en: {db_path}")