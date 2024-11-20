import mysql.connector

def crear_tecnico(connection):
    cursor = connection.cursor()
    dni = input('Ingrese el DNI del técnico:')
    nombre = input('Ingrese el nombre del técnico:')
    apellido = input('Ingrese el apellido del técnico:')
    telefono = input('Ingrese el teléfono del técnico:')
    direccion = input('Ingrese la dirección del técnico:')

    query = ('INSERT INTO tecnico (dni, nombre, apellido, telefono, direccion) '
             'VALUES (%s, %s, %s, %s, %s)')
    cursor.execute(query, (dni, nombre, apellido, telefono, direccion))
    connection.commit()
    print('Técnico insertado correctamente.')

def leer_tecnicos(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM tecnico')
    results = cursor.fetchall()
    for row in results:
        print(row)

def actualizar_tecnico(connection):
    cursor = connection.cursor()
    id_tecnico = input('Ingrese el ID del técnico a actualizar:')
    cursor.execute('SELECT * FROM tecnico WHERE idTecnico = %s', (id_tecnico,))
    print(cursor.fetchall())

    dni = input('Ingrese el nuevo DNI del técnico:')
    nombre = input('Ingrese el nuevo nombre del técnico:')
    apellido = input('Ingrese el nuevo apellido del técnico:')
    telefono = input('Ingrese el nuevo teléfono del técnico:')
    direccion = input('Ingrese la nueva dirección del técnico:')

    query = ('UPDATE tecnico SET dni=%s, nombre=%s, apellido=%s, telefono=%s, direccion=%s '
             'WHERE idTecnico=%s')
    cursor.execute(query, (dni, nombre, apellido, telefono, direccion, id_tecnico))
    connection.commit()
    print('Técnico actualizado correctamente.')

def eliminar_tecnico(connection):
    cursor = connection.cursor()
    id_tecnico = input('Ingrese el ID del técnico a eliminar:')
    query = 'DELETE FROM tecnico WHERE idTecnico = %s'
    cursor.execute(query, (id_tecnico,))
    connection.commit()
    print('Técnico eliminado correctamente.')
