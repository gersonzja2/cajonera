# Sistema de Inventario Cajonera

Este es un sistema de gestión de inventario de escritorio desarrollado en Python para administrar el stock de cartón. Utiliza una arquitectura **Modelo-Vista-Controlador (MVC)**.

## Tecnologías

- **Lenguaje**: Python 3
- **Interfaz Gráfica**: Tkinter
- **Base de Datos**: SQLite
- **ORM**: SQLAlchemy

## Estructura del Proyecto

- `main.py`: Punto de entrada de la aplicación.
- `src/database/connection.py`: Configuración de la base de datos y modelos (Modelo).
- `src/logic/inventario_logic.py`: Lógica de negocio (Controlador).
- `src/ui/`: Ventanas y diálogos (Vistas).
- `data/`: Carpeta contenedora de la base de datos SQLite.

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

4. **Configuración**:
   Asegúrate de tener el archivo `.env` en la raíz con la ruta de la base de datos:
   ```
   DATABASE_URL=sqlite:///data/cajonera.db
   ```

## Ejecución

Para iniciar la aplicación:
```bash
python main.py
```