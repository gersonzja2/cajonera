import tkinter as tk
from tkinter import messagebox
from src.logic.inventario_logic import InventarioLogic

class LoginDialog:
    def __init__(self, parent, on_login_success):
        self.parent = parent
        self.on_login_success = on_login_success
        
        # Crear ventana secundaria (Toplevel)
        self.window = tk.Toplevel(parent)
        self.window.title("Iniciar Sesión")
        self.window.geometry("300x180")
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

    def on_close(self):
        self.parent.destroy()