import tkinter as tk
from tkinter import messagebox

class GestionClientesDialog:
    def __init__(self, parent, logic, on_close_callback):
        self.logic = logic
        self.on_close_callback = on_close_callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Gestión de Clientes")
        self.window.geometry("300x250")
        self.window.transient(parent)
        self.window.grab_set()
        
        tk.Label(self.window, text="Nombre Cliente:").pack(pady=5)
        self.entry_nombre = tk.Entry(self.window)
        self.entry_nombre.pack(pady=5)
        
        tk.Label(self.window, text="Teléfono:").pack(pady=5)
        self.entry_telefono = tk.Entry(self.window)
        self.entry_telefono.pack(pady=5)

        tk.Label(self.window, text="Email:").pack(pady=5)
        self.entry_email = tk.Entry(self.window)
        self.entry_email.pack(pady=5)

        btn_guardar = tk.Button(self.window, text="Guardar Cliente", command=self.guardar)
        btn_guardar.pack(pady=15)
        
    def guardar(self):
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()
        email = self.entry_email.get().strip()

        if not nombre:
            messagebox.showwarning("Error", "El nombre es obligatorio")
            return
            
        exito, mensaje = self.logic.crear_cliente(nombre, telefono, email)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.window.destroy()
            self.on_close_callback()
        else:
            messagebox.showerror("Error", mensaje)