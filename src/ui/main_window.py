import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from src.logic.inventario_logic import InventarioLogic
from src.ui.crear_producto_dialog import CrearProductoDialog
from src.ui.gestion_usuarios_dialog import GestionUsuariosDialog
from src.ui.gestion_clientes_dialog import GestionClientesDialog
from src.ui.gestion_proveedores_dialog import GestionProveedoresDialog
from src.ui.configuracion_dialog import ConfiguracionDialog

class MainWindow:
    def __init__(self, root, usuario, on_logout):
        self.root = root
        self.usuario = usuario
        self.on_logout = on_logout
        self.root.winfo_toplevel().title("Inventario Cajonera")
        self.root.winfo_toplevel().geometry("900x500")
        
        # Instanciar el controlador (Lógica)
        self.logic = InventarioLogic()
        self.carrito = [] # Lista para almacenar items del carrito
        
        self.setup_ui()
        self.actualizar_lista_productos()
        self.actualizar_lista_clientes()
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
            btn_proveedores = tk.Button(frame_prod, text="🚚", command=self.abrir_gestion_proveedores)
            btn_proveedores.pack(side=tk.LEFT, padx=5)
            btn_orden = tk.Button(frame_prod, text="📄", fg="blue", command=self.generar_orden_compra)
            btn_orden.pack(side=tk.LEFT, padx=5)
            btn_config = tk.Button(frame_prod, text="⚙️", command=self.abrir_configuracion)
            btn_config.pack(side=tk.LEFT, padx=5)

        # Display Stock
        self.label_stock = tk.Label(self.root, text="Stock Actual: ...", font=("Arial", 16), fg="#333")
        self.label_stock.pack(pady=20)

        # Frame de Entrada
        frame_entrada = tk.Frame(self.root)
        frame_entrada.pack(pady=10)

        tk.Label(frame_entrada, text="Cantidad:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.entry_cantidad = tk.Entry(frame_entrada, width=10, font=("Arial", 12))
        self.entry_cantidad.pack(side=tk.LEFT, padx=5)

        # Selección de Cliente
        frame_cliente = tk.Frame(self.root)
        frame_cliente.pack(pady=5)
        tk.Label(frame_cliente, text="Cliente:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.combo_clientes = ttk.Combobox(frame_cliente, state="readonly", width=20)
        self.combo_clientes.pack(side=tk.LEFT, padx=5)
        
        btn_add_cliente = tk.Button(frame_cliente, text="+", command=self.abrir_gestion_clientes)
        btn_add_cliente.pack(side=tk.LEFT, padx=2)

        # Frame de Botones
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=30)

        if self.usuario.role == 'admin':
            btn_agregar = tk.Button(frame_botones, text="Llegada de Cargamento (+)", bg="#d4edda", font=("Arial", 10), command=self.agregar)
            btn_agregar.pack(side=tk.LEFT, padx=15)

        # Botón para agregar al carrito en lugar de vender directo
        btn_carrito = tk.Button(frame_botones, text="Agregar al Carrito 🛒", bg="#fff3cd", font=("Arial", 10), command=self.agregar_al_carrito)
        btn_carrito.pack(side=tk.LEFT, padx=15)

        # --- Área del Carrito ---
        frame_carrito = tk.LabelFrame(self.root, text="Carrito de Compras")
        frame_carrito.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree_carrito = ttk.Treeview(frame_carrito, columns=("Producto", "Cantidad", "Precio Unit.", "Subtotal"), show="headings", height=5)
        self.tree_carrito.heading("Producto", text="Producto")
        self.tree_carrito.heading("Cantidad", text="Cantidad")
        self.tree_carrito.heading("Precio Unit.", text="Precio Unit.")
        self.tree_carrito.heading("Subtotal", text="Subtotal")
        
        self.tree_carrito.column("Producto", width=200)
        self.tree_carrito.column("Cantidad", width=80)
        self.tree_carrito.column("Precio Unit.", width=100)
        self.tree_carrito.column("Subtotal", width=100)
        
        self.tree_carrito.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = ttk.Scrollbar(frame_carrito, orient="vertical", command=self.tree_carrito.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.tree_carrito.configure(yscrollcommand=scrollbar.set)

        # Totales y Confirmación
        frame_total = tk.Frame(self.root)
        frame_total.pack(fill="x", padx=10, pady=5)

        self.label_total = tk.Label(frame_total, text="Total a Pagar: $0.00", font=("Arial", 14, "bold"), fg="blue")
        self.label_total.pack(side=tk.LEFT, padx=10)

        btn_confirmar = tk.Button(frame_total, text="Confirmar Venta ✅", bg="#d4edda", font=("Arial", 11, "bold"), command=self.confirmar_venta)
        btn_confirmar.pack(side=tk.RIGHT, padx=5)

        btn_limpiar = tk.Button(frame_total, text="Limpiar 🗑️", bg="#f8d7da", command=self.limpiar_carrito)
        btn_limpiar.pack(side=tk.RIGHT, padx=5)
        
        btn_logout = tk.Button(self.root, text="Cerrar Sesión", command=self.on_logout)
        btn_logout.pack(side=tk.BOTTOM, pady=10)

    def actualizar_lista_productos(self):
        productos = self.logic.obtener_productos()
        self.combo_productos['values'] = productos
        if productos:
            if not self.combo_productos.get():
                self.combo_productos.current(0)

    def actualizar_lista_clientes(self):
        clientes = self.logic.obtener_clientes()
        # Agregamos opción vacía para venta anónima
        self.combo_clientes['values'] = [""] + clientes

    def abrir_crear_producto(self):
        CrearProductoDialog(self.root, self.logic, self.on_producto_creado)

    def on_producto_creado(self):
        self.actualizar_lista_productos()
        self.combo_productos.current(len(self.combo_productos['values']) - 1) # Seleccionar el nuevo
        self.actualizar_display()

    def abrir_gestion_clientes(self):
        GestionClientesDialog(self.root, self.logic, self.actualizar_lista_clientes)

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

    def abrir_gestion_proveedores(self):
        GestionProveedoresDialog(self.root, self.logic)

    def abrir_configuracion(self):
        ConfiguracionDialog(self.root)

    def generar_orden_compra(self):
        # 1. Obtener proveedores para que el usuario elija
        proveedores = self.logic.obtener_proveedores()
        if not proveedores:
            messagebox.showwarning("Atención", "Primero debe registrar al menos un proveedor (Botón 🚚).")
            return

        # 2. Diálogo simple para elegir proveedor (podría ser una ventana más compleja, pero esto funciona)
        # Usamos un Combobox en un diálogo simple o inputdialog, pero simpledialog no tiene combobox nativo fácil.
        # Haremos una ventana emergente rápida personalizada o usamos el primero si solo hay uno, o pedimos escribir el nombre.
        # Para hacerlo profesional, usaremos una ventana Toplevel pequeña para seleccionar.
        self.seleccionar_proveedor_orden(proveedores)

    def ver_ganancias(self):
        ventas, costos, ganancia = self.logic.obtener_reporte_financiero()
        msg = f"--- Reporte Financiero ---\n\n" \
              f"Ingresos Totales:   ${ventas:.2f}\n" \
              f"Costo Mercadería:  -${costos:.2f}\n" \
              f"--------------------------\n" \
              f"Ganancia Neta:      ${ganancia:.2f}"
        messagebox.showinfo("Reporte Financiero", msg)

    def actualizar_display(self):
        producto = self.combo_productos.get()
        if producto:
            datos = self.logic.obtener_datos_producto(producto)
            
            if datos:
                cantidad = datos['cantidad']
                minimo = datos['stock_minimo']
                
                info_precio = f"Precio: ${datos['precio_venta']:.2f} (Margen: ${datos['margen']:.2f})"
                
                # Alerta de stock bajo dinámica (Punto de Reorden)
                if cantidad <= minimo:
                    self.label_stock.config(text=f"Stock: {cantidad} (Mín: {minimo}) ⚠️\n{info_precio}", fg="red")
                else:
                    self.label_stock.config(text=f"Stock: {cantidad} | {info_precio}", fg="#333")
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
        cliente = self.combo_clientes.get() # Puede estar vacío
        
        if not producto:
            messagebox.showwarning("Atención", "Debe seleccionar un producto.")
            return

        if cantidad:
            # Si la función acepta cliente (es venta), lo pasamos
            if accion_func == self.logic.vender_stock:
                exito, mensaje = accion_func(producto, cantidad, self.usuario.username, cliente)
            else:
                exito, mensaje = accion_func(producto, cantidad, self.usuario.username)
            
            if exito:
                messagebox.showinfo(titulo_exito, mensaje)
                self.entry_cantidad.delete(0, tk.END)
                self.actualizar_display()
            else:
                messagebox.showerror("Error", mensaje)

    def agregar(self):
        self.procesar_accion(lambda p, c: self.logic.agregar_stock(p, c, self.usuario.username), "Stock Actualizado")

    def agregar_al_carrito(self):
        cantidad = self.obtener_cantidad()
        producto = self.combo_productos.get()
        
        if not producto:
            messagebox.showwarning("Atención", "Debe seleccionar un producto.")
            return

        if cantidad:
            datos = self.logic.obtener_datos_producto(producto)
            if not datos: return
            
            precio = datos['precio_venta']
            
            # Verificar si ya está en el carrito para sumar cantidad
            encontrado = False
            for item in self.carrito:
                if item['producto'] == producto:
                    item['cantidad'] += cantidad
                    item['subtotal'] = item['cantidad'] * precio
                    encontrado = True
                    break
            
            if not encontrado:
                self.carrito.append({
                    'producto': producto,
                    'cantidad': cantidad,
                    'precio': precio,
                    'subtotal': cantidad * precio
                })
            
            self.actualizar_vista_carrito()
            self.entry_cantidad.delete(0, tk.END)

    def actualizar_vista_carrito(self):
        for item in self.tree_carrito.get_children():
            self.tree_carrito.delete(item)
            
        total_general = 0
        for item in self.carrito:
            self.tree_carrito.insert("", tk.END, values=(item['producto'], item['cantidad'], f"${item['precio']:.2f}", f"${item['subtotal']:.2f}"))
            total_general += item['subtotal']
            
        self.label_total.config(text=f"Total a Pagar: ${total_general:.2f}")

    def limpiar_carrito(self):
        self.carrito = []
        self.actualizar_vista_carrito()

    def confirmar_venta(self):
        if not self.carrito: return
        cliente = self.combo_clientes.get()
        exito, mensaje = self.logic.confirmar_venta_carrito(self.carrito, self.usuario.username, cliente)
        if exito:
            messagebox.showinfo("Venta Exitosa", mensaje)
            self.limpiar_carrito()
            self.actualizar_display()
        else:
            messagebox.showerror("Error", mensaje)

    def seleccionar_proveedor_orden(self, proveedores):
        top = tk.Toplevel(self.root)
        top.title("Generar Orden")
        top.geometry("300x150")
        
        tk.Label(top, text="Seleccione Proveedor:").pack(pady=10)
        combo = ttk.Combobox(top, values=proveedores, state="readonly")
        combo.pack(pady=5)
        if proveedores: combo.current(0)
        
        def confirmar():
            prov = combo.get()
            if prov:
                exito, mensaje = self.logic.generar_orden_compra_pdf(prov)
                if exito: messagebox.showinfo("PDF Generado", mensaje)
                else: messagebox.showerror("Error", mensaje)
                top.destroy()
        
        tk.Button(top, text="Generar PDF", command=confirmar).pack(pady=10)