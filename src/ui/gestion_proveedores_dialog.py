import tkinter as tk
from tkinter import ttk, messagebox

class GestionProveedoresDialog:
    def __init__(self, parent, logic):
        self.logic = logic
        
        self.window = tk.Toplevel(parent)
        self.window.title("Gestión de Proveedores")
        self.window.geometry("400x300")
        self.window.transient(parent.winfo_toplevel())
        self.window.grab_set()
        
        # Frame principal con padding para que no quede pegado a los bordes
        frame = ttk.Frame(self.window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(1, weight=1)
        
        # Widgets usando Grid para mejor alineación
        ttk.Label(frame, text="Nombre Empresa:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_nombre = ttk.Entry(frame)
        self.entry_nombre.grid(row=0, column=1, sticky=tk.EW, pady=5, padx=5)
        
        ttk.Label(frame, text="Contacto (Persona):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_contacto = ttk.Entry(frame)
        self.entry_contacto.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=5)

        ttk.Label(frame, text="Teléfono:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_telefono = ttk.Entry(frame)
        self.entry_telefono.grid(row=2, column=1, sticky=tk.EW, pady=5, padx=5)

        ttk.Label(frame, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.entry_email = ttk.Entry(frame)
        self.entry_email.grid(row=3, column=1, sticky=tk.EW, pady=5, padx=5)

        btn_guardar = ttk.Button(frame, text="Guardar Proveedor", command=self.guardar)
        btn_guardar.grid(row=4, column=0, columnspan=2, pady=20)
        
    def guardar(self):
        nombre = self.entry_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Error", "El nombre es obligatorio")
            return
            
        exito, mensaje = self.logic.crear_proveedor(nombre, self.entry_contacto.get(), self.entry_telefono.get(), self.entry_email.get())
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.window.destroy()
        else:
            messagebox.showerror("Error", mensaje)