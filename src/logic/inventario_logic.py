from src.database.connection import SessionLocal, Producto

class InventarioLogic:
    def __init__(self):
        pass

    def obtener_stock_actual(self):
        """Consulta el stock actual del cartón."""
        session = SessionLocal()
        try:
            producto = session.query(Producto).filter_by(nombre="Carton").first()
            return producto.cantidad if producto else 0
        finally:
            session.close()

    def agregar_stock(self, cantidad):
        """Agrega cantidad al stock existente."""
        session = SessionLocal()
        try:
            producto = session.query(Producto).filter_by(nombre="Carton").first()
            if producto:
                producto.cantidad += cantidad
                session.commit()
                return True, f"Se agregaron {cantidad} unidades."
            return False, "Producto no encontrado en la base de datos."
        except Exception as e:
            session.rollback()
            return False, f"Error de base de datos: {str(e)}"
        finally:
            session.close()

    def vender_stock(self, cantidad):
        """Resta cantidad del stock si hay suficiente."""
        session = SessionLocal()
        try:
            producto = session.query(Producto).filter_by(nombre="Carton").first()
            if producto:
                if producto.cantidad >= cantidad:
                    producto.cantidad -= cantidad
                    session.commit()
                    return True, f"Se vendieron {cantidad} unidades."
                else:
                    return False, "No hay suficiente stock para realizar la venta."
            return False, "Producto no encontrado."
        except Exception as e:
            session.rollback()
            return False, f"Error de base de datos: {str(e)}"
        finally:
            session.close()