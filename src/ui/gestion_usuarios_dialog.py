import tkinter as tk
from tkinter import ttk, messagebox

class GestionUsuariosDialog:
    def __init__(self, parent, logic):
        self.logic = logic
        
        self.window = tk.Toplevel(parent)
        self.window.title("Gestión de Usuarios")
        self.window.geometry("500x450")
        self.window.transient(parent.winfo_toplevel())
        self.window.grab_set()
        
        # --- Lista de Usuarios (Arriba) ---
        frame_lista = tk.LabelFrame(self.window, text="Usuarios Existentes")
        frame_lista.pack(fill="both", expand=True, padx=10, pady=5)
        
        btn_eliminar = tk.Button(frame_lista, text="Eliminar Seleccionado 🗑️", fg="red", command=self.eliminar_usuario)
        btn_eliminar.pack(side=tk.BOTTOM, pady=5)

        self.tree = ttk.Treeview(frame_lista, columns=("Usuario", "Rol"), show="headings", height=8)
        self.tree.heading("Usuario", text="Usuario")
        self.tree.heading("Rol", text="Rol")
        self.tree.column("Usuario", width=200)
        self.tree.column("Rol", width=150)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.tree.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.cargar_usuarios()

        # --- Formulario de Creación (Abajo) ---
        frame_crear = tk.LabelFrame(self.window, text="Crear Nuevo Usuario")
        frame_crear.pack(fill="x", padx=10, pady=10)
        
        tk.Label(frame_crear, text="Usuario:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_user = tk.Entry(frame_crear)
        self.entry_user.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_crear, text="Pass:").grid(row=0, column=2, padx=5, pady=5)
        self.entry_pass = tk.Entry(frame_crear, show="*")
        self.entry_pass.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_crear, text="Rol:").grid(row=1, column=0, padx=5, pady=5)
        self.combo_rol = ttk.Combobox(frame_crear, values=['vendedor', 'almacenista', 'admin'], state="readonly", width=15)
        self.combo_rol.grid(row=1, column=1, padx=5, pady=5)
        self.combo_rol.set('vendedor') # Por defecto, crear usuarios simples

        btn_crear = tk.Button(frame_crear, text="Crear Usuario", command=self.crear_usuario, bg="#d4edda")
        btn_crear.grid(row=1, column=2, columnspan=2, sticky="ew", padx=5, pady=5)

    def cargar_usuarios(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Obtener y llenar
        usuarios = self.logic.obtener_usuarios()
        for u in usuarios:
            self.tree.insert("", tk.END, values=(u['username'], u['role']))

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
            self.cargar_usuarios() # Recargar la lista
        else:
            messagebox.showerror("Error", mensaje)

    def eliminar_usuario(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione un usuario para eliminar.")
            return
        
        username = self.tree.item(selected[0])['values'][0]
        confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al usuario '{username}'?")
        
        if confirm:
            exito, msg = self.logic.eliminar_usuario(username)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self.cargar_usuarios()
            else:
                messagebox.showerror("Error", msg)