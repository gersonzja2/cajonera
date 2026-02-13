import tkinter as tk
from tkinter import ttk

class ReporteFinancieroDialog:
    def __init__(self, parent, logic):
        self.logic = logic
        self.window = tk.Toplevel(parent)
        self.window.title("Reporte Financiero")
        self.window.geometry("400x320")
        self.window.transient(parent.winfo_toplevel())
        self.window.grab_set()
        self.window.resizable(False, False)

        # Título
        tk.Label(self.window, text="Resumen Financiero", font=("Arial", 16, "bold")).pack(pady=20)

        # Frame Contenedor
        frame = tk.Frame(self.window, padx=30)
        frame.pack(fill="both", expand=True)

        # Obtener datos
        ventas, costos, ganancia = self.logic.obtener_reporte_financiero()
        margen = (ganancia / ventas * 100) if ventas > 0 else 0.0

        # Filas de datos
        self._add_row(frame, 0, "Ingresos Totales:", f"${ventas:,.2f}", "green")
        self._add_row(frame, 1, "Costo de Ventas:", f"-${costos:,.2f}", "red")
        
        # Línea separadora
        ttk.Separator(frame, orient="horizontal").grid(row=2, column=0, columnspan=2, sticky="ew", pady=15)

        # Ganancia Neta
        tk.Label(frame, text="Ganancia Neta:", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky="w")
        tk.Label(frame, text=f"${ganancia:,.2f}", font=("Arial", 14, "bold"), fg="blue").grid(row=3, column=1, sticky="e")

        # Margen
        tk.Label(frame, text=f"Margen de Beneficio: {margen:.1f}%", font=("Arial", 9, "italic"), fg="gray").grid(row=4, column=0, columnspan=2, pady=(5, 0))

        # Configurar expansión de columna
        frame.columnconfigure(1, weight=1)

        # Botón Cerrar
        tk.Button(self.window, text="Cerrar", command=self.window.destroy, bg="#e0e0e0", width=10).pack(pady=20)

    def _add_row(self, parent, row, label, value, color):
        tk.Label(parent, text=label, font=("Arial", 11)).grid(row=row, column=0, sticky="w", pady=5)
        tk.Label(parent, text=value, font=("Arial", 11, "bold"), fg=color).grid(row=row, column=1, sticky="e", pady=5)