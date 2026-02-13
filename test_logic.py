import sys
import os

# Agregar el directorio actual al path para poder importar src correctamente
sys.path.append(os.getcwd())

from src.logic.inventario_logic import InventarioLogic

def test_flujo_completo():
    print("--- INICIANDO PRUEBAS AUTOMATIZADAS (SCRIPT) ---")
    
    # 1. Inicializar Lógica
    logic = InventarioLogic()
    # Simulamos ser un administrador para tener permisos
    logic.set_usuario_actual("tester_bot", "admin")
    print("[OK] Lógica instanciada correctamente.")

    # Datos de prueba
    prod_nombre = "Producto Test Script"
    prod_sku = "TEST-SCRIPT-001"
    
    # 2. Crear Producto
    print(f"\n1. Intentando crear producto '{prod_nombre}'...")
    exito, msg = logic.crear_producto(prod_nombre, prod_sku, "General", 50.0, 100.0, 10)
    print(f"   Resultado: {msg}")
    
    # Si falla porque ya existe, no importa, seguimos probando con el existente
    if not exito and "ya existe" not in msg:
        print("   [ERROR CRITICO] No se pudo crear el producto.")
        return

    # 3. Verificar Stock Inicial
    stock_inicial = logic.obtener_stock_actual(prod_nombre)
    print(f"   Stock inicial en DB: {stock_inicial}")

    # 4. Agregar Stock (Prueba de Entrada)
    cantidad_agregar = 10
    print(f"\n2. Agregando {cantidad_agregar} unidades...")
    exito, msg = logic.agregar_stock(prod_nombre, cantidad_agregar, "tester_bot")
    print(f"   Resultado: {msg}")
    
    stock_intermedio = logic.obtener_stock_actual(prod_nombre)
    
    if stock_intermedio == stock_inicial + cantidad_agregar:
        print(f"   [PASS] Stock sumado correctamente. Nuevo stock: {stock_intermedio}")
    else:
        print(f"   [FAIL] Error en suma. Esperado: {stock_inicial + cantidad_agregar}, Real: {stock_intermedio}")

    # 5. Realizar Venta (Prueba de Salida y Finanzas)
    cantidad_vender = 2
    print(f"\n3. Vendiendo {cantidad_vender} unidades...")
    exito, msg = logic.vender_stock(prod_nombre, cantidad_vender, "tester_bot")
    print(f"   Resultado: {msg}")

    stock_final = logic.obtener_stock_actual(prod_nombre)

    if stock_final == stock_intermedio - cantidad_vender:
        print(f"   [PASS] Stock descontado correctamente. Stock final: {stock_final}")
    else:
        print(f"   [FAIL] Error en resta. Esperado: {stock_intermedio - cantidad_vender}, Real: {stock_final}")

    print("\n--- PRUEBAS FINALIZADAS ---")
    print("Revisa 'Documentos/Cajonera/error.log' si algo falló inesperadamente.")

if __name__ == "__main__":
    test_flujo_completo()