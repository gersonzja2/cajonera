import tkinter as tk
from src.database.connection import init_db
from src.ui.login_dialog import LoginDialog
from src.ui.main_window import MainWindow

def main():
    # 1. Inicializar Base de Datos
    init_db()
    
    # 2. Configurar ventana raíz
    root = tk.Tk()
    root.withdraw() # Ocultamos la ventana principal al inicio

    # 3. Función callback para cuando el login es exitoso
    def iniciar_aplicacion(usuario):
        root.deiconify() # Mostrar ventana principal
        MainWindow(root, usuario) # Cargar la vista principal

    # 4. Lanzar Login
    LoginDialog(root, on_login_success=iniciar_aplicacion)
    
    root.mainloop()

if __name__ == "__main__":
    main()