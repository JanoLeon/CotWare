import mysql.connector  # Cambia esto según tu BD (psycopg2, sqlite3, etc.)

class Conexion_BD:
    _connection = None
    _cursor = None

    @classmethod
    def connect(cls):
        """Establece la conexión con la base de datos."""
        if cls._connection is None:
            try:
                cls._connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="tu_base_de_datos"
                )
                cls._cursor = cls._connection.cursor(dictionary=True)  # Devuelve filas como diccionarios (opcional)
                print("Conexión exitosa a la base de datos")
            except mysql.connector.Error as e:
                print(f"Error al conectar a la base de datos: {e}")
                cls._connection = None

    @classmethod
    def get_connection(cls):
        """Obtiene la conexión actual."""
        if cls._connection is None:
            cls.connect()
        return cls._connection

    @classmethod
    def get_cursor(cls):
        """Obtiene el cursor actual."""
        if cls._cursor is None:
            cls.connect()
        return cls._cursor

    @classmethod
    def close_connection(cls):
        """Cierra la conexión con la base de datos."""
        if cls._cursor:
            cls._cursor.close()
            cls._cursor = None
        if cls._connection:
            cls._connection.close()
            cls._connection = None
            print("Conexión cerrada")
