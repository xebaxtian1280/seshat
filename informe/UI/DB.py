import psycopg2
from psycopg2 import sql

class DB:
    def __init__(self, host, database, user, password):
        """
        Constructor para inicializar la conexión a la base de datos.
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def conectar(self):
        """
        Conecta a la base de datos PostgreSQL.
        """
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print("Conexión exitosa a la base de datos.")
        except psycopg2.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.connection = None

    def cerrar_conexion(self):
        """
        Cierra la conexión a la base de datos.
        """
        if self.connection:
            self.connection.close()
            print("Conexión cerrada.")

    def crear_tabla(self, query):
        """
        Crea una tabla en la base de datos.
        :param query: Consulta SQL para crear la tabla.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
                print("Tabla creada exitosamente.")
        except psycopg2.Error as e:
            print(f"Error al crear la tabla: {e}")
            self.connection.rollback()

    def insertar(self, query, valores):
        """
        Inserta un registro en la base de datos.
        :param query: Consulta SQL para insertar datos.
        :param valores: Valores a insertar.
        """
        try:
            with self.connection.cursor() as cursor:
                print(query, valores)
                cursor.execute(query, valores)
                
                # Recuperar el valor devuelto por RETURNING
                recuperado = cursor.fetchone()
                
                self.connection.commit()
                print(f"Registro insertado exitosamente.{recuperado}")
                # Retornar el valor recuperado (si existe)
                return recuperado[0] if recuperado else None
        except psycopg2.Error as e:
            print(f"Error al insertar el registro: {e}")
            self.connection.rollback()
            return None

    def actualizar(self, query, valores):
        """
        Actualiza un registro en la base de datos.
        :param query: Consulta SQL para actualizar datos.
        :param valores: Valores para actualizar.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, valores)
                self.connection.commit()
                print("Registro actualizado exitosamente.")
        except psycopg2.Error as e:
            print(f"Error al actualizar el registro: {e}")
            self.connection.rollback()

    def eliminar(self, query, valores):
        """
        Elimina un registro de la base de datos.
        :param query: Consulta SQL para eliminar datos.
        :param valores: Condiciones para eliminar.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, valores)
                self.connection.commit()
                print("Registro eliminado exitosamente.")
        except psycopg2.Error as e:
            print(f"Error al eliminar el registro: {e}")
            self.connection.rollback()

    def consultar(self, query, valores=None):
        """
        Consulta registros en la base de datos.
        :param query: Consulta SQL para obtener datos.
        :param valores: Condiciones para la consulta (opcional).
        :return: Resultados de la consulta.
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, valores)
                resultados = cursor.fetchall()
                return resultados
        except psycopg2.Error as e:
            print(f"Error al consultar los registros: {e}")
            return None