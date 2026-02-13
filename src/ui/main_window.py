import tkinter as tk
from tkinter import messagebox, ttk
from src.logic.inventario_logic import InventarioLogic
from src.ui.crear_producto_dialog import CrearProductoDialog
from src.ui.gestion_usuarios_dialog import GestionUsuariosDialog

class MainWindow:
    def __init__(self, root, usuario, on_logout):
        self.root = root
        self.usuario = usuario
        self.on_logout = on_logout
        self.root.winfo_toplevel().title("Inventario Cajonera")
        self.root.winfo_toplevel().geometry("450x400")
        
        # Instanciar el controlador (Lógica)
        self.logic = InventarioLogic()
        
        self.setup_ui()
        self.actualizar_lista_productos()
        self.actualizar_display()

    def setup_ui(self):
        # Título
        self.label_titulo = tk.Label(self.root, text="Control de Stock", font=("Arial", 18, "bold"))
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
            btn_eliminar = tk.Button(frame_prod, text="🗑️", fg="red", command=self.eliminar_producto)
            btn_eliminar.pack(side=tk.LEFT, padx=5)
            btn_ganancias = tk.Button(frame_prod, text="💰", fg="green", command=self.ver_ganancias)
            btn_ganancias.pack(side=tk.LEFT, padx=5)
            btn_gestion_usr = tk.Button(frame_prod, text="👤", command=self.abrir_gestion_usuarios)
            btn_gestion_usr.pack(side=tk.LEFT, padx=5)

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

        btn_logout = tk.Button(self.root, text="Cerrar Sesión", command=self.on_logout)
        btn_logout.pack(side=tk.BOTTOM, pady=10)

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

    def eliminar_producto(self):
        producto = self.combo_productos.get()
        if not producto:
            return
        
        confirmar = messagebox.askyesno("Confirmar Baja", f"¿Estás seguro de dar de baja '{producto}'?\nEl historial de ventas se conservará.")
        if confirmar:
            exito, mensaje = self.logic.dar_baja_producto(producto)
            if exito:
                messagebox.showinfo("Baja Exitosa", mensaje)
                self.actualizar_lista_productos()
                self.actualizar_display()
            else:
                messagebox.showerror("Error", mensaje)

    def abrir_gestion_usuarios(self):
        GestionUsuariosDialog(self.root, self.logic)

    def ver_ganancias(self):
        total = self.logic.obtener_reporte_ganancias()
        messagebox.showinfo("Reporte Financiero", f"Total Ingresos por Ventas: ${total:.2f}")

    def actualizar_display(self):
        producto = self.combo_productos.get()
        if producto:
            datos = self.logic.obtener_datos_producto(producto)
            
            if datos:
                cantidad = datos['cantidad']
                minimo = datos['stock_minimo']
                
                # Alerta de stock bajo dinámica (Punto de Reorden)
                if cantidad <= minimo:
                    self.label_stock.config(text=f"Stock: {cantidad} (Mín: {minimo}) ⚠️\nPrecio: ${datos['precio_venta']:.2f}", fg="red")
                else:
                    self.label_stock.config(text=f"Stock: {cantidad} | Precio: ${datos['precio_venta']:.2f}", fg="#333")
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