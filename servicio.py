import mysql.connector

def crear_servicio(connection):
    cursor = connection.cursor()
    nombre = input('Ingrese el nombre del servicio:')
    costo_base = input('Ingrese el costo base del servicio:')

    query = ('INSERT INTO servicio (nombre, costoBase) VALUES (%s, %s)')
    cursor.execute(query, (nombre, costo_base))
    connection.commit()
    print('Servicio insertado correctamente.')

def leer_servicios(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM servicio')
    results = cursor.fetchall()

    # Encabezados de las columnas
    print(f"{'ID':<5} {'Servicio':<25} {'Costo':<10}")
    print("-" * 45)

    for row in results:
        # Formateamos y mostramos cada fila
        id_servicio, nombre_servicio, costo_servicio = row
        print(f"{id_servicio:<5} {nombre_servicio:<25} {costo_servicio:,.2f}")

def actualizar_servicio(connection):
    cursor = connection.cursor()
    id_servicio = input('Ingrese el ID del servicio a actualizar:')
    cursor.execute('SELECT * FROM servicio WHERE idServicio = %s', (id_servicio,))
    print(cursor.fetchall())

    nombre = input('Ingrese el nuevo nombre del servicio:')
    costo_base = input('Ingrese el nuevo costo base del servicio:')

    query = ('UPDATE servicio SET nombre=%s, costoBase=%s WHERE idServicio=%s')
    cursor.execute(query, (nombre, costo_base, id_servicio))
    connection.commit()
    print('Servicio actualizado correctamente.')

def eliminar_servicio(connection):
    cursor = connection.cursor()
    id_servicio = input('Ingrese el ID del servicio a eliminar:')
    query = 'DELETE FROM servicio WHERE idServicio = %s'
    cursor.execute(query, (id_servicio,))
    connection.commit()
    print('Servicio eliminado correctamente.')
