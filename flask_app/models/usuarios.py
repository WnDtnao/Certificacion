"""Consultas y validaciones de cuentas utilizadas por el registro y el acceso."""

import re

from flask_app.config.mysqlconnection import connectToMySQL


class User:
    """Representa a una persona registrada en la aplicación."""

    db = "certificacion"

    def __init__(self, data):
        """Guarda en el objeto los campos que devuelven las consultas SQL."""
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save(cls, data):
        """Inserta una cuenta; la contraseña ya llega cifrada desde el controlador."""
        query = """
            INSERT INTO usuarios
                (nombre, apellido, email, password, created_at, updated_at)
            VALUES
                (%(nombre)s, %(apellido)s, %(email)s, %(password)s, NOW(), NOW());
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_id(cls, user_id):
        """Busca una cuenta por su identificador para validar la sesión."""
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, {"id": user_id})
        if not results:
            return None
        return cls(results[0])

    @classmethod
    def get_by_email(cls, data):
        """Busca una cuenta por correo para registro e inicio de sesión."""
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        email = data.get("email", "").strip().lower()
        results = connectToMySQL(cls.db).query_db(query, {"email": email})
        if not results:
            return None
        return cls(results[0])

    @classmethod
    def validate_register(cls, data):
        """Comprueba los requisitos del formulario antes de guardar una cuenta."""
        nombre = data.get("nombre", "").strip()
        apellido = data.get("apellido", "").strip()
        email = data.get("email", "").strip()
        password = data.get("password", "")
        conf_password = data.get("conf_password", "")

        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not 2 <= len(nombre) <= 45 or not 2 <= len(apellido) <= 45:
            return False
        if not re.fullmatch(email_pattern, email) or len(email) > 254:
            return False
        if (
            not password
            or len(password.encode("utf-8")) > 72
            or password != conf_password
        ):
            return False
        if cls.get_by_email({"email": email.lower()}):
            return False
        return True

    @classmethod
    def validate_login(cls, data):
        """Devuelve la cuenta asociada al correo o indica que no existe."""
        user = cls.get_by_email(
            {"email": data.get("email", "").strip().lower()}
        )
        if not user:
            return False, None
        return True, user
