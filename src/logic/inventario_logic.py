import json
import os
import bcrypt
import re
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from src.database.connection import SessionLocal, Producto, Movimiento, Usuario, Venta, Cliente, Proveedor

class InventarioLogic:
    def __init__(self):
        self.CONFIG_FILE = "config.json"

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

    def vender_stock(self, nombre_producto, cantidad, usuario_id="admin", nombre_cliente=None):
        """Resta cantidad del stock si hay suficiente."""
        session = SessionLocal()
        try:
            producto = session.query(Producto).filter_by(nombre=nombre_producto, activo=True).first()
            if producto:
                if producto.cantidad >= cantidad:
                    # 1. Restar Stock
                    producto.cantidad -= cantidad
                    
                    # Buscar ID del cliente si existe
                    cliente_id = None
                    if nombre_cliente:
                        cliente = session.query(Cliente).filter_by(nombre=nombre_cliente).first()
                        if cliente:
                            cliente_id = cliente.id

                    # 2. Registrar Venta (Financiero)
                    total_venta = producto.precio_venta * cantidad
                    ganancia_venta = (producto.precio_venta - producto.precio_costo) * cantidad
                    nueva_venta = Venta(
                        producto_id=producto.id,
                        cantidad=cantidad,
                        total=total_venta,
                        ganancia=ganancia_venta,
                        usuario_id=usuario_id,
                        cliente_id=cliente_id
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

    def confirmar_venta_carrito(self, items_carrito, usuario_id, nombre_cliente=None):
        """Procesa una lista de items del carrito como una única transacción."""
        session = SessionLocal()
        try:
            # 1. Validar stock para todos los items antes de procesar nada
            # Es mejor hacer esto en un bucle separado para no dejar la sesión en estado sucio si algo falla
            cliente_id = None
            if nombre_cliente:
                cliente = session.query(Cliente).filter_by(nombre=nombre_cliente).first()
                if cliente:
                    cliente_id = cliente.id

            # Bucle de Validación
            for item in items_carrito:
                prod_nombre = item['producto']
                cantidad = item['cantidad']
                
                producto = session.query(Producto).filter_by(nombre=prod_nombre, activo=True).first()
                if not producto:
                    return False, f"Producto '{prod_nombre}' no encontrado."
                if producto.cantidad < cantidad:
                    return False, f"Stock insuficiente para '{prod_nombre}'. Stock: {producto.cantidad}, Solicitado: {cantidad}"

            # 2. Si todo es válido, ejecutamos la operación
            for item in items_carrito:
                prod_nombre = item['producto']
                cantidad = item['cantidad']
                producto = session.query(Producto).filter_by(nombre=prod_nombre, activo=True).first()

                producto.cantidad -= cantidad

                total_venta = producto.precio_venta * cantidad
                ganancia_venta = (producto.precio_venta - producto.precio_costo) * cantidad
                nueva_venta = Venta(
                    producto_id=producto.id,
                    cantidad=cantidad,
                    total=total_venta,
                    ganancia=ganancia_venta,
                    usuario_id=usuario_id,
                    cliente_id=cliente_id
                )
                session.add(nueva_venta)

                nuevo_movimiento = Movimiento(
                    producto_id=producto.id,
                    tipo_movimiento="salida",
                    cantidad=cantidad,
                    usuario_id=usuario_id
                )
                session.add(nuevo_movimiento)

            session.commit()
            return True, "Venta realizada con éxito."

        except Exception as e:
            session.rollback()
            return False, f"Error al procesar venta: {str(e)}"
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

    def obtener_clientes(self):
        """Devuelve una lista con los nombres de todos los clientes."""
        session = SessionLocal()
        try:
            clientes = session.query(Cliente).all()
            return [c.nombre for c in clientes]
        finally:
            session.close()

    def crear_cliente(self, nombre, telefono, email):
        """Crea un nuevo cliente."""
        session = SessionLocal()
        try:
            if session.query(Cliente).filter_by(nombre=nombre).first():
                return False, "El cliente ya existe."
            nuevo = Cliente(nombre=nombre, telefono=telefono, email=email)
            session.add(nuevo)
            session.commit()
            return True, "Cliente registrado correctamente."
        except Exception as e:
            return False, str(e)
        finally:
            session.close()

    def crear_proveedor(self, nombre, contacto, telefono, email):
        """Crea un nuevo proveedor."""
        session = SessionLocal()
        try:
            if session.query(Proveedor).filter_by(nombre=nombre).first():
                return False, "El proveedor ya existe."
            nuevo = Proveedor(nombre=nombre, contacto=contacto, telefono=telefono, email=email)
            session.add(nuevo)
            session.commit()
            return True, "Proveedor registrado correctamente."
        except Exception as e:
            return False, str(e)
        finally:
            session.close()

    def obtener_proveedores(self):
        """Devuelve una lista con los nombres de todos los proveedores."""
        session = SessionLocal()
        try:
            proveedores = session.query(Proveedor).all()
            return [p.nombre for p in proveedores]
        finally:
            session.close()

    def generar_orden_compra_pdf(self, nombre_proveedor):
        """Genera un PDF con los productos que tienen stock bajo."""
        session = SessionLocal()
        try:
            # Buscar productos con stock bajo (cantidad <= stock_minimo)
            productos_bajo_stock = session.query(Producto).filter(Producto.activo == True, Producto.cantidad <= Producto.stock_minimo).all()
            
            if not productos_bajo_stock:
                return False, "No hay productos con stock bajo para pedir."

            # Sanitizar nombre de archivo
            nombre_safe = re.sub(r'[^\w\s-]', '', nombre_proveedor).strip().replace(' ', '_')
            filename = f"Orden_Compra_{nombre_safe}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            # Obtener nombre de la empresa desde config
            config = self.obtener_configuracion()
            empresa = config.get("nombre_empresa", "Mi Empresa")

            c = canvas.Canvas(filename, pagesize=letter)
            
            # Encabezado
            c.setFont("Helvetica-Bold", 16)
            c.drawString(50, 750, f"ORDEN DE COMPRA - {empresa}")
            c.setFont("Helvetica", 12)
            c.drawString(50, 730, f"Proveedor: {nombre_proveedor}")
            c.drawString(50, 715, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

            # Tabla de productos
            y = 680
            c.drawString(50, y, "Producto / SKU")
            c.drawString(300, y, "Stock Actual")
            c.drawString(400, y, "Sugerido a Pedir")
            y -= 20
            c.line(50, y+15, 500, y+15)

            for p in productos_bajo_stock:
                sugerido = (p.stock_minimo * 2) - p.cantidad # Lógica simple: pedir hasta duplicar el mínimo
                if sugerido < 0: sugerido = 0
                
                nombre_display = f"{p.nombre} ({p.codigo})" if p.codigo else p.nombre
                c.drawString(50, y, nombre_display)
                c.drawString(300, y, str(p.cantidad))
                c.drawString(400, y, str(sugerido))
                y -= 20
                
                if y < 50: # Nueva página si se acaba el espacio
                    c.showPage()
                    y = 750

            c.save()
            return True, f"Orden generada: {filename}"
        except Exception as e:
            return False, str(e)
        finally:
            session.close()

    def obtener_historial_ventas(self):
        """Obtiene las ventas recientes para mostrarlas en la tabla de devoluciones."""
        session = SessionLocal()
        try:
            # Unimos Venta con Producto para obtener el nombre
            resultados = session.query(Venta, Producto.nombre).join(Producto, Venta.producto_id == Producto.id).order_by(Venta.fecha_hora.desc()).limit(50).all()
            
            ventas_data = []
            for venta, nombre_prod in resultados:
                ventas_data.append({
                    "id": venta.id,
                    "fecha": venta.fecha_hora.strftime("%d/%m/%Y %H:%M"),
                    "producto": nombre_prod,
                    "cantidad": venta.cantidad,
                    "total": venta.total,
                    "reembolsado": venta.reembolsado
                })
            return ventas_data
        finally:
            session.close()

    def realizar_devolucion(self, venta_id, usuario_id):
        """Procesa la devolución: restaura stock y crea contra-asiento financiero."""
        session = SessionLocal()
        try:
            venta_original = session.query(Venta).get(venta_id)
            if not venta_original:
                return False, "Venta no encontrada."
            if venta_original.reembolsado:
                return False, "Esta venta ya ha sido reembolsada."
            
            # 1. Marcar original como reembolsada
            venta_original.reembolsado = True
            
            # 2. Crear registro negativo en Ventas (Contra-asiento)
            # Esto ajustará automáticamente el reporte financiero (Ingresos - Devoluciones)
            contra_venta = Venta(
                producto_id=venta_original.producto_id,
                cliente_id=venta_original.cliente_id,
                cantidad=-venta_original.cantidad, # Cantidad negativa
                total=-venta_original.total,       # Total negativo (resta de la caja)
                ganancia=-venta_original.ganancia, # Resta de la ganancia
                usuario_id=usuario_id,
                reembolsado=True # Marcamos como true para que no se pueda "devolver la devolución"
            )
            session.add(contra_venta)

            # 3. Restaurar Stock
            producto = session.query(Producto).get(venta_original.producto_id)
            producto.cantidad += venta_original.cantidad

            # 4. Registrar Movimiento de Stock
            movimiento = Movimiento(
                producto_id=venta_original.producto_id,
                tipo_movimiento="devolucion",
                cantidad=venta_original.cantidad,
                usuario_id=usuario_id
            )
            session.add(movimiento)

            session.commit()
            return True, "Devolución procesada correctamente. Stock restaurado y caja ajustada."
        except Exception as e:
            session.rollback()
            return False, str(e)
        finally:
            session.close()

    def obtener_reporte_financiero(self):
        """Calcula ventas totales, costos y ganancia neta."""
        session = SessionLocal()
        try:
            ventas = session.query(Venta).all()
            total_ventas = sum(v.total for v in ventas)
            total_ganancia = sum(v.ganancia for v in ventas)
            total_costos = total_ventas - total_ganancia
            return total_ventas, total_costos, total_ganancia
        finally:
            session.close()

    def obtener_usuarios(self):
        """Devuelve una lista de todos los usuarios y sus roles."""
        session = SessionLocal()
        try:
            usuarios = session.query(Usuario).all()
            return [{"username": u.username, "role": u.role} for u in usuarios]
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

    def obtener_configuracion(self):
        """Lee la configuración desde un archivo JSON."""
        if not os.path.exists(self.CONFIG_FILE):
            return {"nombre_empresa": "Mi Empresa de Cartón"}
        try:
            with open(self.CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            return {"nombre_empresa": "Mi Empresa de Cartón"}

    def guardar_configuracion(self, datos):
        """Guarda la configuración en un archivo JSON."""
        with open(self.CONFIG_FILE, "w") as f:
            json.dump(datos, f, indent=4)
        return True, "Configuración guardada correctamente."