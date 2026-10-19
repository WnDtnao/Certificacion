"""Abre conexiones MySQL y ejecuta consultas parametrizadas para los modelos."""

import os
from pathlib import Path
from threading import Lock

import pymysql
import pymysql.cursors


class MySQLConnection:
    """Administra una conexión y devuelve resultados en formato de diccionario."""

    _database_ready = False
    _initialization_lock = Lock()

    def __init__(self, db):
        # Prepara el esquema una sola vez antes de abrir una conexión a la base.
        self._ensure_database(db)

        # Las credenciales se pueden cambiar sin editar el código fuente.
        self.connection = pymysql.connect(
            host=os.environ.get("MYSQL_HOST", "localhost"),
            user=os.environ.get("MYSQL_USER", "root"),
            password=os.environ.get("MYSQL_PASSWORD", "root"),
            database=db,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )

    @classmethod
    def _ensure_database(cls, db):
        """Crea la base y sus tablas usando el esquema SQL del proyecto."""
        if cls._database_ready:
            return

        with cls._initialization_lock:
            if cls._database_ready:
                return

            connection = pymysql.connect(
                host=os.environ.get("MYSQL_HOST", "localhost"),
                user=os.environ.get("MYSQL_USER", "root"),
                password=os.environ.get("MYSQL_PASSWORD", "root"),
                charset="utf8mb4",
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True,
            )
            try:
                with connection.cursor() as cursor:
                    # Permite iniciar el proyecto aunque el esquema aún no exista.
                    cursor.execute(
                        f"CREATE DATABASE IF NOT EXISTS `{db}` "
                        "DEFAULT CHARACTER SET utf8mb4"
                    )

                    schema_path = Path(__file__).resolve().parents[1] / "bd" / "base.sql"
                    schema_sql = schema_path.read_text(encoding="utf-8")
                    for statement in schema_sql.split(";"):
                        if statement.strip():
                            cursor.execute(statement)
            finally:
                connection.close()

            cls._database_ready = True

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
