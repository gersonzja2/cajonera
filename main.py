import tkinter as tk
from src.database.connection import init_db, backup_db
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
    init_db()
    root = tk.Tk()
    root.title("Sistema de Inventario")
    root.geometry("550x450") # Un poco más ancho para los nuevos botones
    AppController(root)
    root.mainloop()

if __name__ == "__main__":
    main()