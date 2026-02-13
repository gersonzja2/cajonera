import bcrypt
from src.database.connection import SessionLocal, Producto, Movimiento, Usuario, Venta

class InventarioLogic:
    def __init__(self):
        pass

    def obtener_productos(self):
        """Devuelve una lista con los nombres de todos los productos."""
        session = SessionLocal()
        try:
            # READ: Filtro rápido - Solo mostrar productos activos
            productos = session.query(Producto).filter_by(activo=True).all()
            return [p.nombre for p in productos]
        finally:
            session.close()

    def crear_producto(self, nombre, codigo, categoria, costo, precio, stock_min):
        """Crea un nuevo producto en la base de datos."""
        session = SessionLocal()
        try:
            # CREATE: Regla de unicidad para Nombre y Código
            if session.query(Producto).filter_by(nombre=nombre).first():
                return False, "El nombre del producto ya existe."
            if codigo and session.query(Producto).filter_by(codigo=codigo).first():
                return False, "El código (SKU) ya existe."
            
            nuevo_prod = Producto(
                nombre=nombre, 
                codigo=codigo, 
                categoria=categoria, 
                precio_costo=costo,
                precio_venta=precio,
                stock_minimo=stock_min,
                cantidad=0, 
                activo=True
            )
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
            producto = session.query(Producto).filter_by(nombre=nombre_producto, activo=True).first()
            return producto.cantidad if producto else 0
        finally:
            session.close()

    def obtener_datos_producto(self, nombre_producto):
        """Devuelve un diccionario con todos los datos del producto."""
        session = SessionLocal()
        try:
            p = session.query(Producto).filter_by(nombre=nombre_producto, activo=True).first()
            if p:
                margen = p.precio_venta - p.precio_costo
                return {
                    "cantidad": p.cantidad,
                    "stock_minimo": p.stock_minimo,
                    "precio_venta": p.precio_venta,
                    "margen": margen
                }
            return None
        finally:
            session.close()

    def agregar_stock(self, nombre_producto, cantidad, usuario_id="admin"):
        """Agrega cantidad al stock existente de un producto."""
        session = SessionLocal()
        try:
            producto = session.query(Producto).filter_by(nombre=nombre_producto, activo=True).first()
            if producto:
                producto.cantidad += cantidad
                
                # Registrar en historial
                nuevo_movimiento = Movimiento(
                    producto_id=producto.id,
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
            producto = session.query(Producto).filter_by(nombre=nombre_producto, activo=True).first()
            if producto:
                if producto.cantidad >= cantidad:
                    # 1. Restar Stock
                    producto.cantidad -= cantidad
                    
                    # 2. Registrar Venta (Financiero)
                    total_venta = producto.precio_venta * cantidad
                    nueva_venta = Venta(
                        producto_id=producto.id,
                        cantidad=cantidad,
                        total=total_venta,
                        usuario_id=usuario_id
                    )
                    session.add(nueva_venta)

                    # 3. Registrar Historial (Auditoría/Logístico)
                    nuevo_movimiento = Movimiento(
                        producto_id=producto.id,
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

    def dar_baja_producto(self, nombre_producto):
        """DELETE: Borrado Lógico (Soft Delete)."""
        session = SessionLocal()
        try:
            producto = session.query(Producto).filter_by(nombre=nombre_producto).first()
            if producto:
                producto.activo = False # No borramos, solo desactivamos
                session.commit()
                return True, f"Producto '{nombre_producto}' dado de baja correctamente."
            return False, "Producto no encontrado."
        except Exception as e:
            return False, str(e)
        finally:
            session.close()

    def crear_usuario(self, username, password, role):
        """Crea un nuevo usuario en la base de datos."""
        session = SessionLocal()
        try:
            if session.query(Usuario).filter_by(username=username).first():
                return False, f"El usuario '{username}' ya existe."
            
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            nuevo_usuario = Usuario(
                username=username,
                password_hash=hashed.decode('utf-8'),
                role=role
            )
            session.add(nuevo_usuario)
            session.commit()
            return True, f"Usuario '{username}' creado con éxito."
        except Exception as e:
            session.rollback()
            return False, str(e)
        finally:
            session.close()

    def obtener_reporte_ganancias(self):
        """Calcula el total vendido (Solo Admins)."""
        session = SessionLocal()
        try:
            ventas = session.query(Venta).all()
            return sum(v.total for v in ventas)
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