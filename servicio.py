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
    for row in results:
        print(row)

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
