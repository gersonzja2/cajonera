import tkinter as tk
from tkinter import messagebox
from inventario_logic import InventarioLogic

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventario Cajonera - Cartón")
        self.root.geometry("450x400")
        
        # Instanciar el controlador (Lógica)
        self.logic = InventarioLogic()
        
        self.setup_ui()
        self.actualizar_display()

    def setup_ui(self):
        # Título
        self.label_titulo = tk.Label(self.root, text="Control de Stock: Cartón", font=("Arial", 18, "bold"))
        self.label_titulo.pack(pady=20)

        # Display Stock
        self.label_stock = tk.Label(self.root, text="Stock Actual: ...", font=("Arial", 16), fg="#333")
        self.label_stock.pack(pady=20)

        # Frame de Entrada
        frame_entrada = tk.Frame(self.root)
        frame_entrada.pack(pady=10)

        tk.Label(frame_entrada, text="Cantidad:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.entry_cantidad = tk.Entry(frame_entrada, width=10, font=("Arial", 12))
        self.entry_cantidad.pack(side=tk.LEFT, padx=5)

        # Frame de Botones
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=30)

        btn_agregar = tk.Button(frame_botones, text="Llegada de Cargamento (+)", bg="#d4edda", font=("Arial", 10), command=self.agregar)
        btn_agregar.pack(side=tk.LEFT, padx=15)

        btn_vender = tk.Button(frame_botones, text="Venta Realizada (-)", bg="#f8d7da", font=("Arial", 10), command=self.vender)
        btn_vender.pack(side=tk.LEFT, padx=15)

    def actualizar_display(self):
        cantidad = self.logic.obtener_stock_actual()
        self.label_stock.config(text=f"Stock Actual: {cantidad} unidades")

    def obtener_cantidad(self):
        try:
            cantidad = int(self.entry_cantidad.get())
            if cantidad <= 0:
                messagebox.showwarning("Atención", "La cantidad debe ser mayor a 0")
                return None
            return cantidad
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese un número válido")
            return None

    def procesar_accion(self, accion_func, titulo_exito):
        cantidad = self.obtener_cantidad()
        if cantidad:
            exito, mensaje = accion_func(cantidad)
            if exito:
                messagebox.showinfo(titulo_exito, mensaje)
                self.entry_cantidad.delete(0, tk.END)
                self.actualizar_display()
            else:
                messagebox.showerror("Error", mensaje)

    def agregar(self):
        self.procesar_accion(self.logic.agregar_stock, "Stock Actualizado")

    def vender(self):
        self.procesar_accion(self.logic.vender_stock, "Venta Exitosa")