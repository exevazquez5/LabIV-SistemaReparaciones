import mysql.connector

def crear_tecnico(connection):
    cursor = connection.cursor()

     # Validación para el DNI (número de 8 dígitos)
    while True:
        dni = input('Ingrese el DNI del técnico: ')
        if dni.isdigit() and len(dni) == 8:
            break
        else:
            print("El DNI debe ser un número de 8 dígitos.")

     # Validación para el nombre (solo letras)
    while True:
        nombre = input('Ingrese el nombre del técnico: ')
        if nombre.isalpha():
            break
        else:
            print("El nombre solo puede contener letras.")

    # Validación para el apellido (solo letras)
    while True:
        apellido = input('Ingrese el apellido del técnico: ')
        if apellido.isalpha():
            break
        else:
            print("El apellido solo puede contener letras.")

    # Validación para el teléfono (número de 10 dígitos)
    while True:
        telefono = input('Ingrese el teléfono del técnico: ')
        if telefono.isdigit():
            break
        else:
            print("El teléfono debe ser un número valido.")

    # Validación para la dirección (no puede estar vacía)
    while True:
        direccion = input('Ingrese la dirección del técnico: ')
        if direccion.strip():
            break
        else:
            print("La dirección no puede estar vacía.")


    query = ('INSERT INTO tecnico (dni, nombre, apellido, telefono, direccion) '
             'VALUES (%s, %s, %s, %s, %s)')
    cursor.execute(query, (dni, nombre, apellido, telefono, direccion))
    connection.commit()
    print('Técnico insertado correctamente.')

def leer_tecnicos(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM tecnico')
    results = cursor.fetchall()
    
     # Encabezados de las columnas
    print(f"{'ID':<5} {'DNI':<10} {'Nombre':<15} {'Apellido':<15} {'Telefono':<15} {'Direccion':<30}")
    print("-" * 90)  # Línea de separación

    for row in results:
        # Formatear la salida
        id_tecnico, dni, nombre, apellido, telefono, direccion = row
        print(f"{id_tecnico:<5} {dni:<10} {nombre:<15} {apellido:<15} {telefono:<15} {direccion:<30}")

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
