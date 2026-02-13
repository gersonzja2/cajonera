import tkinter as tk
import logging
from tkinter import messagebox
from src.database.connection import init_db, backup_db, setup_logging
from src.ui.login_dialog import LoginDialog
from src.ui.main_window import MainWindow

class AppController:
    def __init__(self, root):
        self.root = root
        self.main_frame = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_close_app)
        self.show_login()

    def show_login(self):
        if self.main_frame:
            backup_db() # Realizar backup al cerrar sesión
            self.main_frame.destroy()
            self.main_frame = None
        self.root.withdraw()
        LoginDialog(self.root, on_login_success=self.show_main_window)

    def show_main_window(self, usuario):
        self.root.deiconify()
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        MainWindow(self.main_frame, usuario, on_logout=self.show_login)

    def on_close_app(self):
        backup_db()
        self.root.destroy()

def main():
    setup_logging()
    try:
        init_db()
        root = tk.Tk()
        root.title("Sistema de Inventario")
        root.geometry("900x500") # Un poco más ancho para los nuevos botones
        app = AppController(root) # Asignar a variable para mantener la referencia
        root.mainloop()
    except Exception as e:
        logging.critical("Error fatal no controlado en la aplicación:", exc_info=True)
        try:
            messagebox.showerror("Error Fatal", f"Se ha producido un error inesperado.\nRevise el log de errores en Documentos/Cajonera.\n\n{str(e)}")
        except:
            pass # Si falla la GUI, al menos queda el log

if __name__ == "__main__":
    main()