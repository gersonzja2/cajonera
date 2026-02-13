import tkinter as tk
from tkinter import messagebox
import os
import platform
import subprocess
from src.logic.inventario_logic import InventarioLogic
from src.database.connection import USER_DIR

class LoginDialog:
    def __init__(self, parent, on_login_success):
        self.parent = parent
        self.on_login_success = on_login_success
        
        # Crear ventana secundaria (Toplevel)
        self.window = tk.Toplevel(parent)
        self.window.title("Iniciar Sesión")
        self.window.geometry("300x250")
        self.window.resizable(False, False)
        
        # Hacer que la ventana sea modal (bloquea la principal)
        self.window.grab_set()
        
        # Widgets
        tk.Label(self.window, text="Usuario:").pack(pady=5)
        self.entry_user = tk.Entry(self.window)
        self.entry_user.pack(pady=5)
        
        tk.Label(self.window, text="Contraseña:").pack(pady=5)
        self.entry_pass = tk.Entry(self.window, show="*")
        self.entry_pass.pack(pady=5)
        
        btn_login = tk.Button(self.window, text="Entrar", command=self.validar, bg="#e0e0e0")
        btn_login.pack(pady=15)
        
        # Botón de acceso rápido a datos y backups
        btn_folder = tk.Button(self.window, text="📂 Abrir Carpeta de Datos", command=self.abrir_carpeta, font=("Arial", 8), fg="blue", bd=0, cursor="hand2")
        btn_folder.pack(side=tk.BOTTOM, pady=10)

        # Protocolo de cierre
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

    def validar(self):
        usuario = self.entry_user.get()
        password = self.entry_pass.get()
        
        logic = InventarioLogic()
        user = logic.autenticar_usuario(usuario, password)
        
        if user:
            self.window.destroy()
            self.on_login_success(user)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    def abrir_carpeta(self):
        """Abre la carpeta de Documentos/Cajonera en el explorador de archivos."""
        path = USER_DIR
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.Popen(["open", path])
        else:  # Linux
            subprocess.Popen(["xdg-open", path])

    def on_close(self):
        self.parent.destroy()