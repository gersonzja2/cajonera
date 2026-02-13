import tkinter as tk
from tkinter import ttk, messagebox

class GestionUsuariosDialog:
    def __init__(self, parent, logic):
        self.logic = logic
        
        self.window = tk.Toplevel(parent)
        self.window.title("Gestión de Usuarios")
        self.window.geometry("300x250")
        self.window.transient(parent.winfo_toplevel())
        self.window.grab_set()
        
        tk.Label(self.window, text="Nombre de Usuario:").pack(pady=5)
        self.entry_user = tk.Entry(self.window)
        self.entry_user.pack(pady=5)
        
        tk.Label(self.window, text="Contraseña:").pack(pady=5)
        self.entry_pass = tk.Entry(self.window, show="*")
        self.entry_pass.pack(pady=5)

        tk.Label(self.window, text="Rol:").pack(pady=5)
        self.combo_rol = ttk.Combobox(self.window, values=['vendedor', 'admin'], state="readonly")
        self.combo_rol.pack(pady=5)
        self.combo_rol.set('vendedor') # Por defecto, crear usuarios simples

        btn_crear = tk.Button(self.window, text="Crear Usuario", command=self.crear_usuario)
        btn_crear.pack(pady=15)

    def crear_usuario(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        role = self.combo_rol.get()

        if not username or not password:
            messagebox.showwarning("Atención", "Usuario y contraseña no pueden estar vacíos.")
            return

        exito, mensaje = self.logic.crear_usuario(username, password, role)
        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.entry_user.delete(0, tk.END)
            self.entry_pass.delete(0, tk.END)
        else:
            messagebox.showerror("Error", mensaje)