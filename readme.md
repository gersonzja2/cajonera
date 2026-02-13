# Sistema de Inventario y POS 

Sistema de gestión de inventario y punto de venta (POS) desarrollado en Python. Diseñado para administrar stock, ventas, clientes y proveedores de manera eficiente utilizando una arquitectura **MVC (Modelo-Vista-Controlador)**.

## Características Principales

- **Gestión de Inventario**: Control de stock en tiempo real, alertas de stock bajo, gestión de productos con SKU, costos y precios.
- **Punto de Venta (POS)**: Carrito de compras para múltiples productos, cálculo automático de totales y validación de stock.
- **Gestión Financiera**: Registro de ventas, cálculo de márgenes de ganancia y reportes financieros (Ingresos vs Costos).
- **Roles de Usuario**: Sistema de login con roles (Admin/Vendedor). Contraseñas encriptadas.
- **Auditoría Avanzada**: Registro detallado de acciones (quién vendió, quién modificó precios, etc.).
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

**Nota:** Los datos de la aplicación (Base de datos, Backups, PDFs y Configuración) se guardan automáticamente en la carpeta **Documentos/Cajonera** del usuario actual para garantizar la persistencia y seguridad de los datos.

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
   *Asegúrate de que `requirements.txt` incluya: `sqlalchemy`, `bcrypt`, `reportlab`.*

4. **Primer Inicio**:
   Al ejecutar la aplicación por primera vez, se creará automáticamente la carpeta `Cajonera` en tus Documentos con la base de datos inicializada.
   
   **Credenciales por defecto:**
   - **Usuario**: `admin`
   - **Contraseña**: `admin`

   **Roles Disponibles:**
   - `admin`: Acceso total.
   - `vendedor`: Solo ventas.
   - `almacenista`: Solo recepción de stock.

## Ejecución

Para iniciar la aplicación:
```bash
python main.py
```