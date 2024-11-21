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

def crear_modelo(connection):
    cursor = connection.cursor()
    nombre = input('Ingrese el nombre del modelo:')
    
    # Mostrar y seleccionar marca
    print("\n=== Selección de Marca ===")
    marcas = mostrar_opciones(cursor, "Marca", ["idMarca", "nombre"])
    while True:
        marca_id = input('\nSeleccione el número de la marca: ').strip()
        marca_id = validar_opcion(marca_id, marcas)
        if marca_id:
            break
        print("Error: Seleccione una marca válida de la lista")

    query = ('INSERT INTO modelo (nombre, Marca_idMarca) VALUES (%s, %s)')
    cursor.execute(query, (nombre, marca_id))
    connection.commit()
    print('Modelo insertado correctamente.')

def leer_modelo(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT m.idModelo, m.nombre, ma.nombre FROM modelo m JOIN marca ma ON m.Marca_idMarca = ma.idMarca')
    results = cursor.fetchall()

    print("Listado de Modelos:")
    print("--------------------")
    
    for row in results:
        # Formato claro y legible
        print(f"ID Modelo: {row[0]:<5} | Nombre: {row[1]:<20} | Marca: {row[2]}")

def actualizar_modelo(connection):
    cursor = connection.cursor()
    id_modelo = input('Ingrese el ID del modelo a actualizar:')
    cursor.execute('SELECT * FROM modelo WHERE idModelo = %s', (id_modelo,))
    modelo = cursor.fetchall()
    if not modelo:
        print('No se encontró un modelo con ese ID.')
        return
    
    print(modelo)
    nombre = input('Ingrese el nuevo nombre del modelo:')
     # Mostrar y seleccionar marca
    print("\n=== Selección de Marca ===")
    marcas = mostrar_opciones(cursor, "Marca", ["idMarca", "nombre"])
    while True:
        marca_id = input('\nSeleccione el número de la marca: ').strip()
        marca_id = validar_opcion(marca_id, marcas)
        if marca_id:
            break
        print("Error: Seleccione una marca válida de la lista")

    
    query = ('UPDATE modelo SET nombre=%s, Marca_idMarca=%s WHERE idModelo=%s ')
    cursor.execute(query, (nombre, marca_id, id_modelo))
    connection.commit()
    print('Modelo actualizado correctamente.')

def eliminar_modelo(connection):
    cursor = connection.cursor()
    id_modelo = input('Ingrese el ID del modelo que desea eliminar:')
    query = 'DELETE FROM modelo WHERE idModelo = %s'
    cursor.execute(query, (id_modelo,))
    connection.commit()
    print('Modelo eliminado con éxito')
