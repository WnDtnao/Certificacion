"""Consultas para las inscripciones entre viajeros y viajes.

Este módulo conserva su ubicación original, aunque ya no gestiona comentarios.
"""

from flask_app.models.peliculas import Trip


def get_travelers(trip_id):
    """Entrega al controlador la lista actualizada de viajeros de un viaje."""
    return Trip.get_travelers(trip_id)
