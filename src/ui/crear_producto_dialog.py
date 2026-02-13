import tkinter as tk
from tkinter import messagebox

class CrearProductoDialog:
    def __init__(self, parent, logic, on_success_callback):
        self.logic = logic
        self.on_success_callback = on_success_callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Nuevo Producto")
        self.window.geometry("300x400")
        self.window.transient(parent)
        self.window.grab_set()
        
        tk.Label(self.window, text="Nombre del Producto:").pack(pady=5)
        self.entry_nombre = tk.Entry(self.window)
        self.entry_nombre.pack(pady=5)
        
        tk.Label(self.window, text="Código (SKU):").pack(pady=5)
        self.entry_codigo = tk.Entry(self.window)
        self.entry_codigo.pack(pady=5)

        tk.Label(self.window, text="Categoría:").pack(pady=5)
        self.entry_categoria = tk.Entry(self.window)
        self.entry_categoria.pack(pady=5)

        tk.Label(self.window, text="Precio Costo ($):").pack(pady=2)
        self.entry_costo = tk.Entry(self.window)
        self.entry_costo.pack(pady=2)

        tk.Label(self.window, text="Precio Venta ($):").pack(pady=2)
        self.entry_precio = tk.Entry(self.window)
        self.entry_precio.pack(pady=2)

        tk.Label(self.window, text="Stock Mínimo (Alerta):").pack(pady=2)
        self.entry_minimo = tk.Entry(self.window)
        self.entry_minimo.pack(pady=2)

        btn_guardar = tk.Button(self.window, text="Guardar", command=self.guardar)
        btn_guardar.pack(pady=15)
        
    def guardar(self):
        try:
            nombre = self.entry_nombre.get().strip()
            codigo = self.entry_codigo.get().strip()
            categoria = self.entry_categoria.get().strip()
            
            # Validar números
            costo = float(self.entry_costo.get())
            precio = float(self.entry_precio.get())
            stock_min = int(self.entry_minimo.get())

            if not nombre:
                messagebox.showwarning("Error", "El nombre no puede estar vacío")
                return
                
            exito, mensaje = self.logic.crear_producto(nombre, codigo, categoria, costo, precio, stock_min)
        except ValueError:
            messagebox.showerror("Error", "Costo, Precio y Stock Mínimo deben ser números válidos.")
            return

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.window.destroy()
            self.on_success_callback()
        else:
            messagebox.showerror("Error", mensaje)