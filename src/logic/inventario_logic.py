import bcrypt
from src.database.connection import SessionLocal, Producto, Movimiento, Usuario

class InventarioLogic:
    def __init__(self):
        pass

    def obtener_productos(self):
        """Devuelve una lista con los nombres de todos los productos."""
        session = SessionLocal()
        try:
            productos = session.query(Producto).all()
            return [p.nombre for p in productos]
        finally:
            session.close()

    def crear_producto(self, nombre):
        """Crea un nuevo producto en la base de datos."""
        session = SessionLocal()
        try:
            if session.query(Producto).filter_by(nombre=nombre).first():
                return False, "El producto ya existe."
            
            nuevo_prod = Producto(nombre=nombre, cantidad=0)
            session.add(nuevo_prod)
            session.commit()
            return True, f"Producto '{nombre}' creado."
        except Exception as e:
            return False, str(e)
        finally:
            session.close()

    def obtener_stock_actual(self, nombre_producto):
        """Consulta el stock actual de un producto específico."""
        session = SessionLocal()
        try:
            producto = session.query(Producto).filter_by(nombre=nombre_producto).first()
            return producto.cantidad if producto else 0
        finally:
            session.close()

    def agregar_stock(self, nombre_producto, cantidad, usuario_id="admin"):
        """Agrega cantidad al stock existente de un producto."""
        session = SessionLocal()
        try:
            producto = session.query(Producto).filter_by(nombre=nombre_producto).first()
            if producto:
                producto.cantidad += cantidad
                
                # Registrar en historial
                nuevo_movimiento = Movimiento(
                    tipo_movimiento="entrada",
                    cantidad=cantidad,
                    usuario_id=usuario_id
                )
                session.add(nuevo_movimiento)
                
                session.commit()
                return True, f"Se agregaron {cantidad} unidades a {nombre_producto}."
            return False, "Producto no encontrado en la base de datos."
        except Exception as e:
            session.rollback()
            return False, f"Error de base de datos: {str(e)}"
        finally:
            session.close()

    def vender_stock(self, nombre_producto, cantidad, usuario_id="admin"):
        """Resta cantidad del stock si hay suficiente."""
        session = SessionLocal()
        try:
            producto = session.query(Producto).filter_by(nombre=nombre_producto).first()
            if producto:
                if producto.cantidad >= cantidad:
                    producto.cantidad -= cantidad
                    
                    # Registrar en historial
                    nuevo_movimiento = Movimiento(
                        tipo_movimiento="salida",
                        cantidad=cantidad,
                        usuario_id=usuario_id
                    )
                    session.add(nuevo_movimiento)
                    
                    session.commit()
                    return True, f"Se vendieron {cantidad} unidades de {nombre_producto}."
                else:
                    return False, f"No hay suficiente stock de {nombre_producto}."
            return False, "Producto no encontrado."
        except Exception as e:
            session.rollback()
            return False, f"Error de base de datos: {str(e)}"
        finally:
            session.close()

    def autenticar_usuario(self, username, password):
        """Verifica las credenciales del usuario."""
        session = SessionLocal()
        try:
            user = session.query(Usuario).filter_by(username=username).first()
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                return user
            return None
        finally:
            session.close()