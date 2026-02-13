import tkinter as tk
from tkinter import ttk, messagebox

class DevolucionesDialog:
    def __init__(self, parent, logic, usuario, on_close_callback):
        self.logic = logic
        self.usuario = usuario
        self.on_close_callback = on_close_callback
        
        self.window = tk.Toplevel(parent)
        self.window.title("Gestión de Devoluciones")
        self.window.geometry("700x400")
        self.window.transient(parent.winfo_toplevel())
        self.window.grab_set()
        
        tk.Label(self.window, text="Historial de Ventas Recientes", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Tabla de Ventas
        frame_tabla = tk.Frame(self.window)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.tree = ttk.Treeview(frame_tabla, columns=("ID", "Fecha", "Producto", "Cant", "Total", "Estado"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Producto", text="Producto")
        self.tree.heading("Cant", text="Cant")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Estado", text="Estado")
        
        self.tree.column("ID", width=50)
        self.tree.column("Fecha", width=120)
        self.tree.column("Producto", width=150)
        self.tree.column("Cant", width=50)
        self.tree.column("Total", width=80)
        self.tree.column("Estado", width=100)
        
        self.tree.pack(side=tk.LEFT, fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        btn_devolver = tk.Button(self.window, text="Devolver Venta Seleccionada ↩️", bg="#f8d7da", command=self.procesar_devolucion)
        btn_devolver.pack(pady=15)
        
        self.cargar_ventas()

    def cargar_ventas(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        ventas = self.logic.obtener_historial_ventas()
        for v in ventas:
            estado = "REEMBOLSADO" if v['reembolsado'] else "Venta"
            # Si la cantidad es negativa, es una devolución (contra-asiento), lo mostramos diferente
            if v['cantidad'] < 0: estado = "Ajuste Devolución"
            
            self.tree.insert("", tk.END, values=(v['id'], v['fecha'], v['producto'], v['cantidad'], f"${v['total']:.2f}", estado))

    def procesar_devolucion(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione una venta para devolver.")
            return
            
        item = self.tree.item(selected[0])
        venta_id = item['values'][0]
        estado = item['values'][5]
        
        if "REEMBOLSADO" in estado or "Ajuste" in estado:
            messagebox.showerror("Error", "No se puede devolver una venta ya reembolsada o un ajuste.")
            return

        confirm = messagebox.askyesno("Confirmar", f"¿Está seguro de devolver la venta ID {venta_id}?\nSe restaurará el stock y se descontará el dinero.")
        if confirm:
            exito, msg = self.logic.realizar_devolucion(venta_id, self.usuario)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self.cargar_ventas()
                self.on_close_callback() # Actualizar stock en ventana principal
            else:
                messagebox.showerror("Error", msg)