import datetime

def mostrar_servicios(cursor):
    cursor.execute("SELECT idServicio, nombre, costoBase FROM servicio")
    servicios = cursor.fetchall()

    print("\nServicios disponibles:")
    print("-" * 50)
    for servicio in servicios:
        print(f"{servicio[0]}. {servicio[1]} - ${servicio[2]:,.2f}")
    print("-" * 50)

    while True:
        servicio_id = input("Seleccione el número del servicio: ")
        if servicio_id.isdigit() and int(servicio_id) in [s[0] for s in servicios]:
            return int(servicio_id)
        print("Opción inválida. Intente de nuevo.")

def mostrar_opciones(cursor, tabla, campos):
    """
    Muestra las opciones disponibles de una tabla
    """
    if tabla == "Dispositivo":
        query = """ 
        SELECT 
            d.idDispositivo,
            d.tipoDispositivo,
            ma.nombre,
            mo.nombre,
            c.nombre,
            c.apellido
        FROM dispositivo d 
        JOIN marca ma ON d.Marca_idMarca = ma.idMarca 
        JOIN modelo mo ON d.Modelo_idModelo = mo.idModelo 
        JOIN cliente c ON d.Cliente_idCliente = c.idCliente
        """
        cursor.execute(query)
        resultados = cursor.fetchall()

        print(f"\nOpciones de {tabla} disponibles:")
        print("-" * 80)
        for resultado in resultados:
            print(f"{resultado[0]:3d}. {resultado[1]} - {resultado[2]} {resultado[3]} - {resultado[4]} {resultado[5]}")
        print("-" * 80)
    else:
        cursor.execute(f"SELECT {', '.join(campos)} FROM {tabla}")
        resultados = cursor.fetchall()
        
        print(f"\nOpciones de {tabla} disponibles:")
        print("-" * 50)
        for resultado in resultados:
            if len(resultado) == 2:  # Para tablas con ID y nombre
                print(f"{resultado[0]:3d}. {resultado[1]}")
            elif len(resultado) == 3:  # Para tabla Cliente
                print(f"{resultado[0]:3d}. {resultado[1]} {resultado[2]}")
            elif len(resultado) == 4:  # Para tabla Tecnico
                print(f"{resultado[0]:3d}. {resultado[1]} {resultado[2]} {resultado[3]}")
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

def crear_reparacion(connection):
    cursor = connection.cursor()
    estado = input('Ingrese el estado de la reparación:')
    descripcion = input('Ingrese la descripción de la reparación:')
    fecha_registro = input('Ingrese la fecha de registro (YYYY-MM-DD):')
    
    # Convertir la fecha de registro a formato correcto
    try:
        fecha_registro = datetime.datetime.strptime(fecha_registro, '%Y-%m-%d').date()
    except ValueError:
        print("Error: Formato de fecha de registro inválido. Debe ser YYYY-MM-DD.")
        return

    # Fechas de inicio y finalización son opcionales
    fecha_inicio = input('Ingrese la fecha de inicio (YYYY-MM-DD, opcional): ')
    fecha_fin = input('Ingrese la fecha de finalización (YYYY-MM-DD, opcional): ')

    if fecha_inicio:
        try:
            fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        except ValueError:
            print("Error: Formato de fecha de inicio inválido. Debe ser YYYY-MM-DD.")
            return
    else:
        fecha_inicio = None

    if fecha_fin:
        try:
            fecha_fin = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        except ValueError:
            print("Error: Formato de fecha de finalización inválido. Debe ser YYYY-MM-DD.")
            return
    else:
        fecha_fin = None

    costo_mano_obra = float(input('Ingrese el costo de mano de obra: '))
    costo_piezas = float(input('Ingrese el costo de las piezas: '))

     # Mostrar y seleccionar Dispositivo
    print("\n=== Selección de Dispositivo ===")
    dispositivos = mostrar_opciones(cursor, "Dispositivo", [])
    while True:
        dispositivo_id = input('\nSeleccione el número del dispositivo: ').strip()
        dispositivo_id = validar_opcion(dispositivo_id, dispositivos)
        if dispositivo_id:
            break
        print("Error: Seleccione un dispositivo válido de la lista")

    # Mostrar y seleccionar Técnico
    print("\n=== Selección de Técnico ===")
    tecnicos = mostrar_opciones(cursor, "tecnico", ["idTecnico", "dni", "nombre", "apellido"])
    while True:
        tecnico_id = input('\nSeleccione el número del técnico: ').strip()
        tecnico_id = validar_opcion(tecnico_id, tecnicos)
        if tecnico_id:
            break
        print("Error: Seleccione una marca válida de la lista")

    # Defino el servicio y los muestro
    servicio_id = mostrar_servicios(cursor)

    cursor.execute("SELECT costoBase FROM servicio WHERE idServicio = %s", (servicio_id,))
    servicio_precio = cursor.fetchone()[0]

    costo_total = costo_mano_obra + costo_piezas + servicio_precio

    print(f"\nCosto Total: ${costo_total:,.2f}")

    query = ('INSERT INTO reparacion (estado, descripcion, fechaRegistro, fechaInicio, fechaFin, '
             'costoManoObra, costoPiezas, Dispositivo_idDispositivo, Tecnico_idTecnico) '
             'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)')
    
    # Insertar registro en tabla intermedia
    cursor.execute("INSERT INTO reparacion_has_servicio (Reparacion_idReparacion, Servicio_idServicio) VALUES (%s, %s)",
                   (cursor.lastrowid, servicio_id))
    
    cursor.execute(query, (estado, descripcion, fecha_registro, fecha_inicio, fecha_fin,
                           costo_mano_obra, costo_piezas, dispositivo_id, tecnico_id))
    connection.commit()
    print('Reparación insertada correctamente.')

def leer_reparaciones(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM reparacion')
    reparaciones = cursor.fetchall()

    print("\nListado de Reparaciones:")
    print("-" * 80)

    for reparacion in reparaciones:
        id_reparacion, estado, descripcion, fecha_registro, fecha_inicio, fecha_fin, costo_mano_obra, costo_piezas, dispositivo_id, tecnico_id = reparacion

        print(f"ID: {id_reparacion}")
        print(f"Estado: {estado}")
        print(f"Descripción: {descripcion}")
        print(f"Fecha Registro: {fecha_registro}")
        print(f"Fecha Inicio: {fecha_inicio if fecha_inicio else '-'}")
        print(f"Fecha Fin: {fecha_fin if fecha_fin else '-'}")
        print(f"Costo Mano de Obra: ${costo_mano_obra:,.0f}")
        print(f"Costo Piezas: ${costo_piezas:,.0f}")
        print(f"Dispositivo: {dispositivo_id}")
        print(f"Técnico: {tecnico_id}")
        print("-" * 80)

def actualizar_reparacion(connection):
    cursor = connection.cursor()
    id_reparacion = input('Ingrese el ID de la reparación a actualizar:')
    cursor.execute('SELECT * FROM reparacion WHERE idReparacion = %s', (id_reparacion,))
    reparacion = cursor.fetchall()
    if not reparacion:
        print('No se encontró una reparación con ese ID.')
        return
    
    print(reparacion)
    estado = input('Ingrese el nuevo estado de la reparación:')
    descripcion = input('Ingrese la nueva descripción de la reparación:')
    fecha_inicio = input('Ingrese la nueva fecha de inicio (YYYY-MM-DD):')
    fecha_fin = input('Ingrese la nueva fecha de finalización (YYYY-MM-DD):')
    costo_mano_obra = input('Ingrese el nuevo costo de mano de obra:')
    costo_piezas = input('Ingrese el nuevo costo de las piezas:')
    id_dispositivo = input('Ingrese el nuevo ID del dispositivo:')
    id_tecnico = input('Ingrese el nuevo ID del técnico:')
    
    query = ('UPDATE reparacion SET estado=%s, descripcion=%s, fechaInicio=%s, fechaFin=%s, '
             'costoManoObra=%s, costoPiezas=%s, Dispositivo_idDispositivo=%s, Tecnico_idTecnico=%s '
             'WHERE idReparacion=%s')
    cursor.execute(query, (estado, descripcion, fecha_inicio, fecha_fin, costo_mano_obra, costo_piezas,
                           id_dispositivo, id_tecnico, id_reparacion))
    connection.commit()
    print('Reparación actualizada correctamente.')

def eliminar_reparacion(connection):
    cursor = connection.cursor()
    id_reparacion = input('Ingrese el ID de la reparación a eliminar:')
    cursor.execute('SELECT * FROM reparacion WHERE idReparacion = %s', (id_reparacion,))
    reparacion = cursor.fetchall()
    if not reparacion:
        print('No se encontró una reparación con ese ID.')
        return

    query = 'DELETE FROM reparacion WHERE idReparacion = %s'
    cursor.execute(query, (id_reparacion,))
    connection.commit()
    print('Reparación eliminada con éxito.')
