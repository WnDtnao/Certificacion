from datetime import date

from flask_app.config.mysqlconnection import connectToMySQL


class Trip:
    db = "certificacion"

    def __init__(self, data):
        self.id = data["id"]
        self.destino = data["destino"]
        self.fecha_inicio = data["fecha_inicio"]
        self.fecha_fin = data["fecha_fin"]
        self.itinerario = data["itinerario"]
        self.organizador_id = data["organizador_id"]
        self.organizador = data["organizador"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all(cls):
        # solo viajes que todavia no empiezan, del mas cercano al mas lejano
        query = """
            SELECT viajes.*, usuarios.nombre AS organizador
            FROM viajes
            JOIN usuarios ON viajes.organizador_id = usuarios.id
            WHERE viajes.fecha_inicio >= CURDATE()
            ORDER BY viajes.fecha_inicio ASC, viajes.id ASC;
        """
        rows = connectToMySQL(cls.db).query_db(query)
        return [cls(row) for row in rows]

    @classmethod
    def get_by_id(cls, trip_id):
        query = """
            SELECT viajes.*, usuarios.nombre AS organizador
            FROM viajes
            JOIN usuarios ON viajes.organizador_id = usuarios.id
            WHERE viajes.id = %(id)s;
        """
        rows = connectToMySQL(cls.db).query_db(query, {"id": trip_id})
        if not rows:
            return None
        return cls(rows[0])

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO viajes
                (destino, fecha_inicio, fecha_fin, itinerario, organizador_id, created_at, updated_at)
            VALUES
                (%(destino)s, %(fecha_inicio)s, %(fecha_fin)s, %(itinerario)s, %(organizador_id)s, NOW(), NOW());
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = """
            UPDATE viajes
            SET destino = %(destino)s,
                fecha_inicio = %(fecha_inicio)s,
                fecha_fin = %(fecha_fin)s,
                itinerario = %(itinerario)s,
                updated_at = NOW()
            WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, trip_id):
        query = "DELETE FROM viajes WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, {"id": trip_id})

    @classmethod
    def get_travelers(cls, trip_id):
        query = """
            SELECT usuarios.id, usuarios.nombre, usuarios.apellido
            FROM viajeros
            JOIN usuarios ON viajeros.usuario_id = usuarios.id
            WHERE viajeros.viaje_id = %(id)s
            ORDER BY usuarios.nombre, usuarios.apellido;
        """
        return connectToMySQL(cls.db).query_db(query, {"id": trip_id})

    @classmethod
    def is_traveler(cls, trip_id, user_id):
        query = """
            SELECT id FROM viajeros
            WHERE viaje_id = %(viaje_id)s AND usuario_id = %(usuario_id)s;
        """
        rows = connectToMySQL(cls.db).query_db(
            query, {"viaje_id": trip_id, "usuario_id": user_id}
        )
        return bool(rows)

    @classmethod
    def join(cls, trip_id, user_id):
        query = """
            INSERT INTO viajeros (viaje_id, usuario_id, created_at)
            VALUES (%(viaje_id)s, %(usuario_id)s, NOW());
        """
        return connectToMySQL(cls.db).query_db(
            query, {"viaje_id": trip_id, "usuario_id": user_id}
        )

    @classmethod
    def leave(cls, trip_id, user_id):
        query = """
            DELETE FROM viajeros
            WHERE viaje_id = %(viaje_id)s AND usuario_id = %(usuario_id)s;
        """
        return connectToMySQL(cls.db).query_db(
            query, {"viaje_id": trip_id, "usuario_id": user_id}
        )

    @staticmethod
    def validate(data):
        destino = data.get("destino", "").strip()
        itinerario = data.get("itinerario", "").strip()
        inicio_texto = data.get("fecha_inicio", "").strip()
        fin_texto = data.get("fecha_fin", "").strip()
        if not destino or len(destino) > 120 or not itinerario or len(itinerario) > 40:
            return False
        try:
            inicio = date.fromisoformat(inicio_texto)
            fin = date.fromisoformat(fin_texto)
        except ValueError:
            return False
        return inicio >= date.today() and fin > inicio
