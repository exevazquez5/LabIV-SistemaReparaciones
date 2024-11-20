import os
import mysql.connector
from mysql.connector import Error

# Importar las funciones CRUD de cada módulo
from cliente import crear_cliente, leer_clientes, actualizar_cliente, eliminar_cliente
from dispositivo import crear_dispositivo, leer_dispositivos, actualizar_dispositivo, eliminar_dispositivo
from marca import crear_marca, leer_marcas, actualizar_marca, eliminar_marca
from modelo import crear_modelo, leer_modelo, actualizar_modelo, eliminar_modelo
from reparacion import crear_reparacion, leer_reparaciones, actualizar_reparacion, eliminar_reparacion
from tecnico import crear_tecnico, leer_tecnicos, actualizar_tecnico, eliminar_tecnico
from servicio import crear_servicio, leer_servicios, actualizar_servicio, eliminar_servicio

def conectar():
    try:
        # Conexion a la base de datos
        connection = mysql.connector.connect(
            host='localhost',
            database='sistemareparaciones',
            user='root',
            password='admin'
        )
        return connection
    except Error as e:
        print(f'Error al conectar a la base de datos: {e}')
    return None

def menu_tabla():
    print('\n--- Selección de Tabla ---')
    print('1. Cliente')
    print('2. Dispositivo')
    print('3. Reparación')
    print('4. Técnico')
    print('5. Servicio')
    print('6. Marca')
    print('7. Modelo')
    print('8. Salir')
    tabla_opcion = input('Seleccione la tabla con la que desea trabajar: ')

    os.system('cls' if os.name == 'nt' else 'clear')    

    return tabla_opcion

def menu_operacion():
    print('\n--- Operaciones CRUD ---')
    print('1. Crear registro')
    print('2. Leer registros')
    print('3. Actualizar registro')
    print('4. Eliminar registro')
    print('5. Volver al menú principal')
    operacion_opcion = input('Seleccione una operación: ')

    os.system('cls' if os.name == 'nt' else 'clear')    
    
    return operacion_opcion

def menu():
    conexion = conectar()
    if not conexion:
        return
    
    while True:
        tabla_opcion = menu_tabla()

        if tabla_opcion == '1':  # Cliente
            while True:
                operacion_opcion = menu_operacion()
                if operacion_opcion == '1':
                    crear_cliente(conexion)
                elif operacion_opcion == '2':
                    leer_clientes(conexion)
                elif operacion_opcion == '3':
                    actualizar_cliente(conexion)
                elif operacion_opcion == '4':
                    eliminar_cliente(conexion)
                elif operacion_opcion == '5':
                    break
                else:
                    print('Opción no válida. Intente de nuevo.')

        elif tabla_opcion == '2':  # Dispositivo
            while True:
                operacion_opcion = menu_operacion()
                if operacion_opcion == '1':
                    crear_dispositivo(conexion)
                elif operacion_opcion == '2':
                    leer_dispositivos(conexion)
                elif operacion_opcion == '3':
                    actualizar_dispositivo(conexion)
                elif operacion_opcion == '4':
                    eliminar_dispositivo(conexion)
                elif operacion_opcion == '5':
                    break
                else:
                    print('Opción no válida. Intente de nuevo.')

        elif tabla_opcion == '3':  # Reparación
            while True:
                operacion_opcion = menu_operacion()
                if operacion_opcion == '1':
                    crear_reparacion(conexion)
                elif operacion_opcion == '2':
                    leer_reparaciones(conexion)
                elif operacion_opcion == '3':
                    actualizar_reparacion(conexion)
                elif operacion_opcion == '4':
                    eliminar_reparacion(conexion)
                elif operacion_opcion == '5':
                    break
                else:
                    print('Opción no válida. Intente de nuevo.')

        elif tabla_opcion == '4':  # Técnico
            while True:
                operacion_opcion = menu_operacion()
                if operacion_opcion == '1':
                    crear_tecnico(conexion)
                elif operacion_opcion == '2':
                    leer_tecnicos(conexion)
                elif operacion_opcion == '3':
                    actualizar_tecnico(conexion)
                elif operacion_opcion == '4':
                    eliminar_tecnico(conexion)
                elif operacion_opcion == '5':
                    break
                else:
                    print('Opción no válida. Intente de nuevo.')

        elif tabla_opcion == '5':  # Servicio
            while True:
                operacion_opcion = menu_operacion()
                if operacion_opcion == '1':
                    crear_servicio(conexion)
                elif operacion_opcion == '2':
                    leer_servicios(conexion)
                elif operacion_opcion == '3':
                    actualizar_servicio(conexion)
                elif operacion_opcion == '4':
                    eliminar_servicio(conexion)
                elif operacion_opcion == '5':
                    break
                else:
                    print('Opción no válida. Intente de nuevo.')

        elif tabla_opcion == '6':  # Marca
            while True:
                operacion_opcion = menu_operacion()
                if operacion_opcion == '1':
                    crear_marca(conexion)
                elif operacion_opcion == '2':
                    leer_marcas(conexion)
                elif operacion_opcion == '3':
                    actualizar_marca(conexion)
                elif operacion_opcion == '4':
                    eliminar_marca(conexion)
                elif operacion_opcion == '5':
                    break
                else:
                    print('Opción no válida. Intente de nuevo.')

        elif tabla_opcion == '7':  # Modelo
            while True:
                operacion_opcion = menu_operacion()
                if operacion_opcion == '1':
                    crear_modelo(conexion)
                elif operacion_opcion == '2':
                    leer_modelo(conexion)
                elif operacion_opcion == '3':
                    actualizar_modelo(conexion)
                elif operacion_opcion == '4':
                    eliminar_modelo(conexion)
                elif operacion_opcion == '5':
                    break
                else:
                    print('Opción no válida. Intente de nuevo.')

        elif tabla_opcion == '8':  # Salir
            conexion.close()
            print('Conexión cerrada. Saliendo del programa...')
            break

        else:
            print('Opción no válida. Intente de nuevo.')

if __name__ == '__main__':
    menu()
