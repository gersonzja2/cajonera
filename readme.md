# Sistema de Inventario y POS 

Sistema de gestión de inventario y punto de venta (POS) desarrollado en Python. Diseñado para administrar stock, ventas, clientes y proveedores de manera eficiente utilizando una arquitectura **MVC (Modelo-Vista-Controlador)**.

## Características Principales

- **Gestión de Inventario**: Control de stock en tiempo real, alertas de stock bajo, gestión de productos con SKU, costos y precios.
- **Punto de Venta (POS)**: Carrito de compras para múltiples productos, cálculo automático de totales y validación de stock.
- **Gestión Financiera**: Registro de ventas, cálculo de márgenes de ganancia y reportes financieros (Ingresos vs Costos).
- **Roles de Usuario**: Sistema de login con roles (Admin/Vendedor). Contraseñas encriptadas.
- **Gestión de Terceros**: Base de datos de Clientes y Proveedores.
- **Automatización**: Generación de Órdenes de Compra en PDF y copias de seguridad automáticas de la base de datos.

## Tecnologías

- **Lenguaje**: Python 3
- **Interfaz Gráfica**: Tkinter (con widgets ttk)
- **Base de Datos**: SQLite
- **ORM**: SQLAlchemy
- **Reportes**: ReportLab (PDF)
- **Seguridad**: Bcrypt

## Estructura del Proyecto

- `main.py`: Punto de entrada. Gestiona el ciclo de vida de la app.
- `src/database/connection.py`: Modelos de base de datos y configuración.
- `src/logic/inventario_logic.py`: Lógica de negocio y controladores.
- `src/ui/`: Interfaces gráficas (Ventana principal, diálogos de gestión).
- `data/`: Almacenamiento de la base de datos (`cajonera.db`).
- `backups/`: Copias de seguridad automáticas.

## Instalación y Configuración

1. **Crear un entorno virtual**:
   ```bash
   python -m venv venv
   ```

2. **Activar el entorno virtual**:
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
   *Asegúrate de que `requirements.txt` incluya: `sqlalchemy`, `python-dotenv`, `bcrypt`, `reportlab`.*

4. **Configuración**:
   El sistema crea automáticamente la base de datos en `data/cajonera.db` al iniciar.
   
   **Credenciales por defecto:**
   - **Usuario**: `admin`
   - **Contraseña**: `admin`

## Ejecución

Para iniciar la aplicación:
```bash
python main.py
```