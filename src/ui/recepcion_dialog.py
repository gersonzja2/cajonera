import tkinter as tk
from tkinter import ttk, messagebox

class RecepcionDialog:
    def __init__(self, parent, logic, usuario, on_close_callback):
        self.logic = logic
        self.usuario = usuario
        self.on_close_callback = on_close_callback
        self.items = []

        self.window = tk.Toplevel(parent)
        self.window.title("Recepción de Cargamento")
        self.window.geometry("600x450")
        self.window.transient(parent.winfo_toplevel())
        self.window.grab_set()

        tk.Label(self.window, text="Ingreso de Mercadería", font=("Arial", 14, "bold")).pack(pady=10)

        # --- Área de Selección ---
        frame_input = tk.Frame(self.window)
        frame_input.pack(pady=5)

        tk.Label(frame_input, text="Producto:").pack(side=tk.LEFT, padx=5)
        self.combo_productos = ttk.Combobox(frame_input, state="readonly", width=25)
        self.combo_productos.pack(side=tk.LEFT, padx=5)
        self.combo_productos['values'] = self.logic.obtener_productos()
        if self.combo_productos['values']: self.combo_productos.current(0)

        tk.Label(frame_input, text="Cantidad:").pack(side=tk.LEFT, padx=5)
        self.entry_cantidad = tk.Entry(frame_input, width=10)
        self.entry_cantidad.pack(side=tk.LEFT, padx=5)

        btn_add = tk.Button(frame_input, text="Agregar a Lista", command=self.agregar_item, bg="#d4edda")
        btn_add.pack(side=tk.LEFT, padx=10)

        # --- Lista de Recepción ---
        frame_lista = tk.LabelFrame(self.window, text="Lista de Entrada")
        frame_lista.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(frame_lista, columns=("Producto", "Cantidad"), show="headings")
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Cantidad", text="Cantidad a Ingresar")
        self.tree.column("Producto", width=300)
        self.tree.column("Cantidad", width=150)
        self.tree.pack(side=tk.LEFT, fill="both", expand=True)

        # --- Botones de Acción ---
        frame_botones = tk.Frame(self.window)
        frame_botones.pack(pady=15)

        btn_confirmar = tk.Button(frame_botones, text="Confirmar Recepción ✅", font=("Arial", 11, "bold"), bg="#28a745", fg="white", command=self.confirmar)
        btn_confirmar.pack(side=tk.LEFT, padx=20)

        btn_cancelar = tk.Button(frame_botones, text="Cancelar", command=self.window.destroy)
        btn_cancelar.pack(side=tk.LEFT, padx=20)

    def agregar_item(self):
        producto = self.combo_productos.get()
        try:
            cantidad = int(self.entry_cantidad.get())
            if cantidad <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida mayor a 0.")
            return

        if not producto: return

        # Verificar si ya está en la lista
        for item in self.items:
            if item['producto'] == producto:
                item['cantidad'] += cantidad
                self.actualizar_lista()
                self.entry_cantidad.delete(0, tk.END)
                return

        self.items.append({'producto': producto, 'cantidad': cantidad})
        self.actualizar_lista()
        self.entry_cantidad.delete(0, tk.END)

    def actualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for item in self.items:
            self.tree.insert("", tk.END, values=(item['producto'], item['cantidad']))

    def confirmar(self):
        if not self.items: return
        exito, msg = self.logic.confirmar_recepcion(self.items, self.usuario)
        if exito:
            messagebox.showinfo("Éxito", msg)
            self.on_close_callback() # Actualizar stock en ventana principal
            self.window.destroy()
        else:
            messagebox.showerror("Error", msg)