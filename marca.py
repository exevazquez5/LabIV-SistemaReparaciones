import mysql.connector

def crear_marca(connection):
    cursor = connection.cursor()
    nombre = input('Ingrese el nombre de la marca:')

    query = ('INSERT INTO marca (nombre) VALUES (%s)')
    cursor.execute(query, (nombre, ))
    connection.commit()
    print('Marca insertada correctamente.')

def leer_marcas(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM marca')
    results = cursor.fetchall()
    
    print("Listado de Marcas:")
    print("-------------------")
    
    for row in results:
        # Asumiendo que row[0] es el ID y row[1] es el nombre de la marca
        print(f"ID: {row[0]}, Marca: {row[1]}")

def actualizar_marca(connection):
    cursor = connection.cursor()
    id_marca = input('Ingrese el ID de la marca a actualizar:')
    cursor.execute('SELECT * FROM marca WHERE idMarca = %s', (id_marca,))
    marca = cursor.fetchall()
    if not marca:
        print('No se encontró una marca con ese ID.')
        return
    
    print(marca)
    nombre = input('Ingrese el nuevo nombre de la marca:')
    
    query = ('UPDATE marca SET nombre=%s WHERE idMarca=%s ')
    cursor.execute(query, (nombre, id_marca))
    connection.commit()
    print('Marca actualizada correctamente.')

def eliminar_marca(connection):
    cursor = connection.cursor()
    id_marca= input('Ingrese el ID de la marca que desea eliminar:')

    try:
        query_eliminar_marca = "DELETE FROM marca WHERE idMarca = %s"
        cursor.execute(query_eliminar_marca, (id_marca,))
        connection.commit()
        print("Marca eliminada correctamente.")
    
    except mysql.connector.Error as err:
        if err.errno == 1451:
            print("No se puede eliminar la marca porque está siendo utilizada por dispositivos.")
        else:
            print(f"Error al eliminar: {err}")
        connection.rollback()

    finally:
        cursor.close()
