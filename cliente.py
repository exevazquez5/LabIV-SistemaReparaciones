def crear_cliente(connection):
    cursor = connection.cursor()
    nombre = input('Ingrese un nombre:')
    apellido = input('Ingrese un apellido:')

    while True:
        telefono = input('Ingrese un telefono: ')
        if telefono.isdigit():  # Verifica si el teléfono contiene solo números
            break
        else:
            print("Error: El teléfono solo debe contener números.")
    
    direccion = input('Ingrese una direccion:')
    
    # Crear la query
    query = ('INSERT INTO cliente (nombre, apellido, telefono, direccion) VALUES (%s, %s, %s, %s)')
    # Ejecutar la consulta de INSERT en la tabla cliente
    cursor.execute(query, (nombre, apellido, telefono, direccion))
    connection.commit()

    print('Registro insertado correctamente.')

def leer_clientes(connection):
    cursor = connection.cursor()

    # Crear la query
    cursor.execute('SELECT * FROM cliente')

    # Imprimir los resultados
    results = cursor.fetchall()
    for row in results:
        print(row)

def actualizar_cliente(connection):
    cursor = connection.cursor()
    # Solicitar el idCliente
    id_registro = input('Ingrese el id del cliente:')
    # Mostrar los datos del cliente seleccionado
    cursor.execute('SELECT idCliente, nombre, apellido, telefono, direccion FROM cliente WHERE idCliente = %s;', (id_registro,))
    results = cursor.fetchall()
    print(results)
    # Permitir ingresar el resto de datos al usuario
    nombre = input('Ingrese un nombre:')
    apellido = input('Ingrese un apellido:')
    telefono = input('Ingrese un telefono:')
    direccion = input('Ingrese una direccion:')

    # Crear la query
    query = 'UPDATE cliente SET nombre=%s, apellido=%s, telefono=%s, direccion=%s WHERE idCliente=%s;'
    cursor.execute(query, (nombre, apellido, telefono, direccion, id_registro))
    connection.commit()

    print('Registro actualizado exitosamente.')

def eliminar_cliente(connection):
    cursor = connection.cursor()
    id_cliente = input('Ingrese el id del cliente que desea eliminar:')
    
    # Crear la query
    query = 'DELETE FROM cliente WHERE idCliente = %s;'
    cursor.execute(query, (id_cliente,))
    connection.commit()

    print('Registro eliminado con éxito')
