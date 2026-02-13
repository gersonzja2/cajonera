import tkinter as tk
from tkinter import messagebox
from src.logic.inventario_logic import InventarioLogic

class ConfiguracionDialog:
    def __init__(self, parent):
        self.logic = InventarioLogic()
        self.window = tk.Toplevel(parent)
        self.window.title("Configuración")
        self.window.geometry("350x250")
        self.window.transient(parent.winfo_toplevel())
        self.window.grab_set()
        
        tk.Label(self.window, text="Configuración del Sistema", font=("Arial", 14, "bold")).pack(pady=20)
        
        # Cargar configuración actual
        config = self.logic.obtener_configuracion()
        
        tk.Label(self.window, text="Nombre de la Empresa (para PDF):").pack(pady=5)
        self.entry_empresa = tk.Entry(self.window, width=40)
        self.entry_empresa.pack(pady=5)
        self.entry_empresa.insert(0, config.get("nombre_empresa", ""))
        
        btn_guardar = tk.Button(self.window, text="Guardar Cambios", command=self.guardar, bg="#d4edda")
        btn_guardar.pack(pady=20)

    def guardar(self):
        nombre = self.entry_empresa.get().strip()
        if nombre:
            datos = {"nombre_empresa": nombre}
            exito, msg = self.logic.guardar_configuracion(datos)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self.window.destroy()