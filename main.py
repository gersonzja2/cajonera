import tkinter as tk
from tkinter import messagebox
from database import init_db, SessionLocal, Producto

class InventarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventario Cajonera - Cartón")
        self.root.geometry("400x350")
        
        # Inicializar base de datos
        init_db()
        
        # Estilos y Widgets
        self.label_titulo = tk.Label(root, text="Control de Stock: Cartón", font=("Arial", 16, "bold"))
        self.label_titulo.pack(pady=10)

        self.label_stock = tk.Label(root, text="Stock Actual: Cargando...", font=("Arial", 14))
        self.label_stock.pack(pady=20)

        # Frame para entrada de datos
        frame_entrada = tk.Frame(root)
        frame_entrada.pack(pady=10)

        tk.Label(frame_entrada, text="Cantidad:").pack(side=tk.LEFT, padx=5)
        self.entry_cantidad = tk.Entry(frame_entrada, width=10)
        self.entry_cantidad.pack(side=tk.LEFT, padx=5)

        # Botones
        frame_botones = tk.Frame(root)
        frame_botones.pack(pady=20)

        btn_agregar = tk.Button(frame_botones, text="Llegada de Cargamento (+)", bg="#d4edda", command=self.agregar_stock)
        btn_agregar.pack(side=tk.LEFT, padx=10)

        btn_vender = tk.Button(frame_botones, text="Venta Realizada (-)", bg="#f8d7da", command=self.vender_stock)
        btn_vender.pack(side=tk.LEFT, padx=10)

        # Actualizar vista inicial
        self.actualizar_display()

    def get_session(self):
        return SessionLocal()

    def actualizar_display(self):
        session = self.get_session()
        producto = session.query(Producto).filter_by(nombre="Carton").first()
        if producto:
            self.label_stock.config(text=f"Stock Actual: {producto.cantidad} unidades")
        session.close()

    def obtener_cantidad_input(self):
        try:
            cantidad = int(self.entry_cantidad.get())
            if cantidad <= 0:
                messagebox.showwarning("Error", "La cantidad debe ser mayor a 0")
                return None
            return cantidad
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un número válido")
            return None

    def agregar_stock(self):
        cantidad = self.obtener_cantidad_input()
        if cantidad:
            session = self.get_session()
            producto = session.query(Producto).filter_by(nombre="Carton").first()
            if producto:
                producto.cantidad += cantidad
                session.commit()
                messagebox.showinfo("Éxito", f"Se agregaron {cantidad} unidades.")
                self.entry_cantidad.delete(0, tk.END)
            session.close()
            self.actualizar_display()

    def vender_stock(self):
        cantidad = self.obtener_cantidad_input()
        if cantidad:
            session = self.get_session()
            producto = session.query(Producto).filter_by(nombre="Carton").first()
            
            if producto:
                if producto.cantidad >= cantidad:
                    producto.cantidad -= cantidad
                    session.commit()
                    messagebox.showinfo("Venta", f"Se vendieron {cantidad} unidades.")
                    self.entry_cantidad.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", "No hay suficiente stock para esta venta.")
            
            session.close()
            self.actualizar_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = InventarioApp(root)
    root.mainloop()