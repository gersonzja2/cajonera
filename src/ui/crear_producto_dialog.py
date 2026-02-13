import tkinter as tk
from tkinter import messagebox

class CrearProductoDialog:
    def __init__(self, parent, logic, on_success_callback):
        self.logic = logic
        self.on_success_callback = on_success_callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Nuevo Producto")
        self.window.geometry("300x150")
        self.window.transient(parent)
        self.window.grab_set()
        
        tk.Label(self.window, text="Nombre del Producto:").pack(pady=5)
        self.entry_nombre = tk.Entry(self.window)
        self.entry_nombre.pack(pady=5)
        
        btn_guardar = tk.Button(self.window, text="Guardar", command=self.guardar)
        btn_guardar.pack(pady=15)
        
    def guardar(self):
        nombre = self.entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Error", "El nombre no puede estar vacío")
            return
            
        exito, mensaje = self.logic.crear_producto(nombre)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.window.destroy()
            self.on_success_callback()
        else:
            messagebox.showerror("Error", mensaje)