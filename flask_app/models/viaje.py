from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime, date

class Viaje:

    def __init__(self, data):
        self.id = data['id']
        self.destino = data['destino']
        self.fecha_inicio = data['fecha_inicio']
        self.fecha_fin = data['fecha_fin']
        self.itinerario = data['itinerario']
        self.usuario_id = data['usuario_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # nombre del que organiza, viene del JOIN
        self.organizador = data['organizador']

    # solo los viajes que no han empezado, el mas cercano primero
    @classmethod
    def get_all(cls):
        query = "SELECT viajes.*, usuarios.nombre AS organizador FROM viajes JOIN usuarios ON viajes.usuario_id = usuarios.id WHERE viajes.fecha_inicio >= CURDATE() ORDER BY viajes.fecha_inicio ASC;"
        resultados = connectToMySQL('certificacion').query_db(query)
        viajes = []
        for viaje in resultados:
            viajes.append(cls(viaje))
        return viajes

    @classmethod
    def get_one(cls, data):
        query = "SELECT viajes.*, usuarios.nombre AS organizador FROM viajes JOIN usuarios ON viajes.usuario_id = usuarios.id WHERE viajes.id = %(id)s;"
        resultado = connectToMySQL('certificacion').query_db(query, data)
        if len(resultado) < 1:
            return False
        return cls(resultado[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO viajes (destino, fecha_inicio, fecha_fin, itinerario, usuario_id, created_at, updated_at) VALUES (%(destino)s, %(fecha_inicio)s, %(fecha_fin)s, %(itinerario)s, %(usuario_id)s, NOW(), NOW());"
        return connectToMySQL('certificacion').query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE viajes SET destino = %(destino)s, fecha_inicio = %(fecha_inicio)s, fecha_fin = %(fecha_fin)s, itinerario = %(itinerario)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('certificacion').query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM viajes WHERE id = %(id)s;"
        return connectToMySQL('certificacion').query_db(query, data)

    # ---- viajeros (tabla intermedia) ----

    @classmethod
    def get_viajeros(cls, data):
        query = "SELECT usuarios.id, usuarios.nombre, usuarios.apellido FROM viajeros JOIN usuarios ON viajeros.usuario_id = usuarios.id WHERE viajeros.viaje_id = %(id)s;"
        return connectToMySQL('certificacion').query_db(query, data)

    @classmethod
    def unirse(cls, data):
        query = "INSERT INTO viajeros (usuario_id, viaje_id, created_at) VALUES (%(usuario_id)s, %(viaje_id)s, NOW());"
        return connectToMySQL('certificacion').query_db(query, data)

    @classmethod
    def cancelar(cls, data):
        query = "DELETE FROM viajeros WHERE usuario_id = %(usuario_id)s AND viaje_id = %(viaje_id)s;"
        return connectToMySQL('certificacion').query_db(query, data)

    @staticmethod
    def validar_viaje(formulario):
        es_valido = True

        if len(formulario['destino']) < 1:
            flash("El Destino es obligatorio", "viaje")
            es_valido = False
        if len(formulario['itinerario']) < 1:
            flash("El Itinerario es obligatorio", "viaje")
            es_valido = False
        elif len(formulario['itinerario']) > 40:
            flash("El Itinerario no puede tener más de 40 caracteres", "viaje")
            es_valido = False

        if formulario['fecha_inicio'] == "" or formulario['fecha_fin'] == "":
            flash("Las fechas son obligatorias", "viaje")
            return False

        inicio = datetime.strptime(formulario['fecha_inicio'], '%Y-%m-%d').date()
        fin = datetime.strptime(formulario['fecha_fin'], '%Y-%m-%d').date()
        if inicio < date.today():
            flash("La fecha de inicio no puede ser en el pasado", "viaje")
            es_valido = False
        if fin <= inicio:
            flash("La fecha de fin debe ser después de la fecha de inicio", "viaje")
            es_valido = False

        return es_valido
