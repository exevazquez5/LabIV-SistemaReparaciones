from mysql.connector import Error

def mostrar_opciones(cursor, tabla, campos):
    """
    Muestra las opciones disponibles de una tabla
    """
    cursor.execute(f"SELECT {', '.join(campos)} FROM {tabla}")
    resultados = cursor.fetchall()
    
    print(f"\nOpciones de {tabla} disponibles:")
    print("-" * 50)
    for resultado in resultados:
        if len(resultado) == 2:  # Para tablas con ID y nombre
            print(f"{resultado[0]:3d}. {resultado[1]}")
        elif len(resultado) == 3:  # Para tabla Cliente
            print(f"{resultado[0]:3d}. {resultado[1]} {resultado[2]}")
    print("-" * 50)
    return resultados

def validar_opcion(opcion, resultados):
    """
    Valida que la opción ingresada exista en los resultados
    """
    try:
        opcion = int(opcion)
        ids_validos = [r[0] for r in resultados]
        if opcion not in ids_validos:
            return None
        return opcion
    except ValueError:
        return None

def crear_dispositivo(connection):
    cursor = None
    try:
        cursor = connection.cursor()

        # Solicitar tipo de dispositivo
        while True:
            tipo = input('\nIngrese el tipo de dispositivo: ').strip()
            if tipo and 2 <= len(tipo) <= 50:
                break
            print("Error: El tipo debe tener entre 2 y 50 caracteres")

        # Mostrar y seleccionar marca
        print("\n=== Selección de Marca ===")
        marcas = mostrar_opciones(cursor, "Marca", ["idMarca", "nombre"])
        while True:
            marca_id = input('\nSeleccione el número de la marca: ').strip()
            marca_id = validar_opcion(marca_id, marcas)
            if marca_id:
                break
            print("Error: Seleccione una marca válida de la lista")

        # Mostrar y seleccionar modelo
        print("\n=== Selección de Modelo ===")
        # Filtrar modelos por marca seleccionada
        cursor.execute("""
            SELECT idModelo, nombre 
            FROM Modelo 
            WHERE Marca_idMarca = %s
        """, (marca_id,))
        modelos = cursor.fetchall()
        
        if not modelos:
            print(f"No hay modelos registrados para esta marca.")
            return
            
        print("\nModelos disponibles para la marca seleccionada:")
        print("-" * 50)
        for modelo in modelos:
            print(f"{modelo[0]:3d}. {modelo[1]}")
        print("-" * 50)
        
        while True:
            modelo_id = input('\nSeleccione el número del modelo: ').strip()
            modelo_id = validar_opcion(modelo_id, modelos)
            if modelo_id:
                break
            print("Error: Seleccione un modelo válido de la lista")

        # Mostrar y seleccionar cliente
        print("\n=== Selección de Cliente ===")
        clientes = mostrar_opciones(cursor, "Cliente", ["idCliente", "nombre", "apellido"])
        while True:
            cliente_id = input('\nSeleccione el número del cliente: ').strip()
            cliente_id = validar_opcion(cliente_id, clientes)
            if cliente_id:
                break
            print("Error: Seleccione un cliente válido de la lista")

        # Crear el dispositivo
        query = """
        INSERT INTO Dispositivo (tipoDispositivo, Marca_idMarca, Modelo_idModelo, Cliente_idCliente) 
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (tipo, marca_id, modelo_id, cliente_id))
        connection.commit()

        # Mostrar confirmación con los detalles
        cursor.execute("""
            SELECT 
                d.tipoDispositivo,
                m.nombre as marca,
                mo.nombre as modelo,
                CONCAT(c.nombre, ' ', c.apellido) as cliente
            FROM Dispositivo d
            JOIN Marca m ON d.Marca_idMarca = m.idMarca
            JOIN Modelo mo ON d.Modelo_idModelo = mo.idModelo
            JOIN Cliente c ON d.Cliente_idCliente = c.idCliente
            WHERE d.idDispositivo = LAST_INSERT_ID()
        """)
        dispositivo = cursor.fetchone()
        
        print("\n¡Registro creado exitosamente!")
        print("-" * 50)
        print(f"Tipo: {dispositivo[0]}")
        print(f"Marca: {dispositivo[1]}")
        print(f"Modelo: {dispositivo[2]}")
        print(f"Cliente: {dispositivo[3]}")
        print("-" * 50)

    except Error as e:
        connection.rollback()
        print(f"Error al crear dispositivo: {str(e)}")
    finally:
        if cursor:
            cursor.close()

def leer_dispositivos(connection):
    cursor = connection.cursor()
    query = '''
        SELECT 
            d.idDispositivo, 
            d.tipoDispositivo, 
            m.nombre AS marca, 
            mo.nombre AS modelo, 
            c.nombre AS cliente_nombre, 
            c.apellido AS cliente_apellido
        FROM 
            dispositivo d
        JOIN 
            marca m ON d.Marca_idMarca = m.idMarca
        JOIN 
            modelo mo ON d.Modelo_idModelo = mo.idModelo
        JOIN 
            cliente c ON d.Cliente_idCliente = c.idCliente
    '''
    cursor.execute(query)
    results = cursor.fetchall()
    
     # Encabezados de las columnas
    print(f"{'ID Dispositivo':<15} {'Tipo':<12} {'Marca':<15} {'Modelo':<15} {'Cliente':<25}")
    print("-" * 85)  # Línea de separación

    for row in results:
        # Formatear la salida
        id_dispositivo, tipo, marca, modelo, cliente_nombre, cliente_apellido = row
        print(f"{id_dispositivo:<15} {tipo:<12} {marca:<15} {modelo:<15} {cliente_nombre} {cliente_apellido}")

def actualizar_dispositivo(connection):
    cursor = connection.cursor()
    id_dispositivo = input('Ingrese el ID del dispositivo a actualizar:')
    cursor.execute('SELECT * FROM dispositivo WHERE idDispositivo = %s', (id_dispositivo,))
    print(cursor.fetchall())
    
    tipo_dispositivo = input('Ingrese el nuevo tipo de dispositivo:')
    id_marca = input('Ingrese el nuevo ID de la marca:')
    id_modelo = input('Ingrese el nuevo ID del modelo:')
    id_cliente = input('Ingrese el nuevo ID del cliente asociado:')
    
    query = ('UPDATE dispositivo SET tipoDispositivo=%s, Marca_idMarca=%s, Modelo_idModelo=%s, '
             'Cliente_idCliente=%s WHERE idDispositivo=%s')
    cursor.execute(query, (tipo_dispositivo, id_marca, id_modelo, id_cliente, id_dispositivo))
    connection.commit()
    print('Dispositivo actualizado correctamente.')

def eliminar_dispositivo(connection):
    cursor = connection.cursor()
    id_dispositivo = input('Ingrese el ID del dispositivo que desea eliminar:')
    query = 'DELETE FROM dispositivo WHERE idDispositivo = %s'
    cursor.execute(query, (id_dispositivo,))
    connection.commit()
    print('Dispositivo eliminado con éxito')
