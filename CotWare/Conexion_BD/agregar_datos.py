import bcrypt
from db_conexion import Conexion_BD  # Asegúrate de que la clase Conexion_BD esté en el mismo proyecto

def agregar_empleado(nombre, rut, telefono, cargo, departamento):
    """Agrega un empleado a las tablas datos_empleados y login_empleados."""
    # Generar correo basado en el nombre y apellido
    nombre_partes = nombre.split()
    if len(nombre_partes) < 2:
        print("El nombre debe tener al menos un nombre y un apellido.")
        return
    correo = f"{nombre_partes[0].lower()}.{nombre_partes[1].lower()}@cotware.cl"

    # Generar contraseña cifrada
    contrasena_plana = "Contraseña123"  # Puedes cambiarla o generarla aleatoriamente
    contrasena_cifrada = bcrypt.hashpw(contrasena_plana.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Insertar datos en la tabla datos_empleados
    query_datos_empleados = """
        INSERT INTO datos_empleados (Nombre_Empleado, RUT_Empleado, Telefono_Empleado, Cargo_Empleado, Departamento_Empleado)
        VALUES (%s, %s, %s, %s, %s)
    """
    query_login_empleados = """
        INSERT INTO login_empleados (Correo, Contraseña, ID_Empleado)
        VALUES (%s, %s, %s)
    """
    conexion = Conexion_BD.get_connection()
    cursor = conexion.cursor()

    try:
        # Insertar en datos_empleados
        cursor.execute(query_datos_empleados, (nombre, rut, telefono, cargo, departamento))
        conexion.commit()

        # Obtener el ID del empleado recién insertado
        id_empleado = cursor.lastrowid

        # Insertar en login_empleados
        cursor.execute(query_login_empleados, (correo, contrasena_cifrada, id_empleado))
        conexion.commit()

        print(f"Empleado '{nombre}' agregado correctamente con correo '{correo}'.")
    except Exception as e:
        conexion.rollback()
        print(f"Error al agregar el empleado: {e}")
    finally:
        if cursor:
            cursor.close()

# Datos de los empleados
empleados = [
    ("Manuel Calderon", "21605737-6", "997942666", "Programador", "Desarrollo"),
    ("Monserrat Kerber", "21512194-1", "928409914", "Marketing", "Comunicaciones"),
    ("Benjamin Hermosilla", "21305714-6", "938933272", "Programador", "Desarrollo")
]

# Paso 1: Conectar a la base de datos cotware
Conexion_BD.connect()  # Conectamos a la base de datos cotware

# Paso 2: Agregar empleados
for empleado in empleados:
    agregar_empleado(*empleado)

# Paso 3: Cerrar la conexión al finalizar
Conexion_BD.close_connection()
