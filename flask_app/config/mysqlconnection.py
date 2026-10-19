"""Abre conexiones MySQL y ejecuta consultas parametrizadas para los modelos."""

import os

import pymysql
import pymysql.cursors


class MySQLConnection:
    """Administra una conexión y devuelve resultados en formato de diccionario."""

    def __init__(self, db):
        # Las credenciales se pueden cambiar sin editar el código fuente.
        self.connection = pymysql.connect(
            host=os.environ.get("MYSQL_HOST", "localhost"),
            user=os.environ.get("MYSQL_USER", "root"),
            password=os.environ.get("MYSQL_PASSWORD", ""),
            database=db,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )

    def query_db(self, query, data=None):
        """Ejecuta una consulta, devuelve filas/ID o indica si fue exitosa."""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, data)
                if cursor.description is not None:
                    return cursor.fetchall()
                if cursor.lastrowid:
                    return cursor.lastrowid
                return True
        finally:
            # Cada instancia representa una sola consulta; se libera al terminar.
            self.connection.close()


def connectToMySQL(db):
    """Crea la conexión que utilizan las consultas de los modelos."""
    return MySQLConnection(db)
