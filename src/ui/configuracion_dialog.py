import tkinter as tk
from tkinter import messagebox

class ConfiguracionDialog:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Configuración")
        self.window.geometry("350x250")
        self.window.transient(parent.winfo_toplevel())
        self.window.grab_set()
        
        tk.Label(self.window, text="Configuración del Sistema", font=("Arial", 14, "bold")).pack(pady=20)
        
        # Aquí puedes agregar opciones futuras
        tk.Label(self.window, text="Opciones disponibles próximamente:\n\n- Ruta de Copia de Seguridad\n- Tema de la Aplicación\n- Datos de la Empresa (para PDF)", justify=tk.LEFT).pack(pady=10)
        
        btn_cerrar = tk.Button(self.window, text="Cerrar", command=self.window.destroy)
        btn_cerrar.pack(pady=20)