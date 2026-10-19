"""Rutas para que cada viajero se inscriba o cancele su participación."""

from datetime import date

from flask import abort, flash, redirect, session, url_for

from flask_app import app
from flask_app.models.peliculas import Trip


@app.route("/viaje/<int:trip_id>/unirme", methods=["POST"])
def unirme_viaje(trip_id):
    """Inscribe al usuario autenticado una sola vez en un viaje futuro."""
    if "user_id" not in session:
        return redirect(url_for("index"))

    trip = Trip.get_by_id(trip_id)
    if not trip:
        return redirect(url_for("dashboard"))
    if trip.organizador_id == session["user_id"]:
        flash("La persona organizadora no necesita inscribirse como viajera.", "viaje")
        return redirect(url_for("ver_viaje", trip_id=trip_id))
    if trip.fecha_inicio < date.today():
        flash("Ya no es posible inscribirse en un viaje que comenzó.", "viaje")
        return redirect(url_for("ver_viaje", trip_id=trip_id))

    if not Trip.is_traveler(trip_id, session["user_id"]):
        if not Trip.join(trip_id, session["user_id"]):
            abort(500)
    return redirect(url_for("ver_viaje", trip_id=trip_id))


@app.route("/viaje/<int:trip_id>/cancelar", methods=["POST"])
def cancelar_viaje(trip_id):
    """Retira de la lista únicamente a la persona que pulsa Cancelar."""
    if "user_id" not in session:
        return redirect(url_for("index"))

    trip = Trip.get_by_id(trip_id)
    if not trip:
        return redirect(url_for("dashboard"))
    if Trip.is_traveler(trip_id, session["user_id"]):
        if not Trip.leave(trip_id, session["user_id"]):
            abort(500)
    return redirect(url_for("ver_viaje", trip_id=trip_id))
