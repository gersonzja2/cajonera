import tkinter as tk
from tkinter import messagebox, ttk
from src.logic.inventario_logic import InventarioLogic
from src.ui.crear_producto_dialog import CrearProductoDialog

class MainWindow:
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario
        self.root.title("Inventario Cajonera - Cartón")
        self.root.geometry("450x400")
        
        # Instanciar el controlador (Lógica)
        self.logic = InventarioLogic()
        
        self.setup_ui()
        self.actualizar_lista_productos()
        self.actualizar_display()

    def setup_ui(self):
        # Título
        self.label_titulo = tk.Label(self.root, text="Control de Stock: Cartón", font=("Arial", 18, "bold"))
        self.label_titulo.pack(pady=20)

        # Selección de Producto
        frame_prod = tk.Frame(self.root)
        frame_prod.pack(pady=5)
        
        tk.Label(frame_prod, text="Producto:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        
        self.combo_productos = ttk.Combobox(frame_prod, state="readonly", width=20)
        self.combo_productos.pack(side=tk.LEFT, padx=5)
        self.combo_productos.bind("<<ComboboxSelected>>", lambda e: self.actualizar_display())
        
        if self.usuario.role == 'admin':
            btn_nuevo = tk.Button(frame_prod, text="+", command=self.abrir_crear_producto)
            btn_nuevo.pack(side=tk.LEFT, padx=5)

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

        if self.usuario.role == 'admin':
            btn_agregar = tk.Button(frame_botones, text="Llegada de Cargamento (+)", bg="#d4edda", font=("Arial", 10), command=self.agregar)
            btn_agregar.pack(side=tk.LEFT, padx=15)

        btn_vender = tk.Button(frame_botones, text="Venta Realizada (-)", bg="#f8d7da", font=("Arial", 10), command=self.vender)
        btn_vender.pack(side=tk.LEFT, padx=15)

    def actualizar_lista_productos(self):
        productos = self.logic.obtener_productos()
        self.combo_productos['values'] = productos
        if productos:
            if not self.combo_productos.get():
                self.combo_productos.current(0)

    def abrir_crear_producto(self):
        CrearProductoDialog(self.root, self.logic, self.on_producto_creado)

    def on_producto_creado(self):
        self.actualizar_lista_productos()
        self.combo_productos.current(len(self.combo_productos['values']) - 1) # Seleccionar el nuevo
        self.actualizar_display()

    def actualizar_display(self):
        producto = self.combo_productos.get()
        if producto:
            cantidad = self.logic.obtener_stock_actual(producto)
            
            # Alerta de stock bajo (menos de 50 unidades)
            if cantidad < 50:
                self.label_stock.config(text=f"Stock Actual ({producto}): {cantidad} unidades ⚠️", fg="red")
            else:
                self.label_stock.config(text=f"Stock Actual ({producto}): {cantidad} unidades", fg="#333")
        else:
            self.label_stock.config(text="Stock Actual: -", fg="#333")

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
        producto = self.combo_productos.get()
        
        if not producto:
            messagebox.showwarning("Atención", "Debe seleccionar un producto.")
            return

        if cantidad:
            exito, mensaje = accion_func(producto, cantidad)
            if exito:
                messagebox.showinfo(titulo_exito, mensaje)
                self.entry_cantidad.delete(0, tk.END)
                self.actualizar_display()
            else:
                messagebox.showerror("Error", mensaje)

    def agregar(self):
        self.procesar_accion(lambda p, c: self.logic.agregar_stock(p, c, self.usuario.username), "Stock Actualizado")

    def vender(self):
        self.procesar_accion(lambda p, c: self.logic.vender_stock(p, c, self.usuario.username), "Venta Exitosa")