"""Rutas para crear, consultar, editar y borrar viajes."""

from flask import abort, flash, redirect, render_template, request, session, url_for

from flask_app import app
from flask_app.models.comentarios import get_travelers
from flask_app.models.peliculas import Trip
from flask_app.models.usuarios import User


@app.route("/dashboard")
@app.route("/viajes")
@app.route("/cine")
def dashboard():
    """Muestra los viajes futuros y comprueba que la sesión siga vigente."""
    if "user_id" not in session:
        return redirect(url_for("index"))

    user = User.get_by_id(session["user_id"])
    if not user:
        session.clear()
        return redirect(url_for("index"))

    return render_template("registro.html", viajes=Trip.get_all())


@app.route("/nuevo")
@app.route("/cine/nueva")
def nuevo_viaje():
    """Abre el formulario de creación para una persona autenticada."""
    if "user_id" not in session:
        return redirect(url_for("index"))
    return render_template("nuevapeli.html")


@app.route("/crear", methods=["POST"])
@app.route("/cine/crear", methods=["POST"])
def crear_viaje():
    """Valida y registra un viaje asignando a la persona actual como organizadora."""
    if "user_id" not in session:
        return redirect(url_for("index"))

    data = {
        "destino": request.form.get("destino", "").strip(),
        "fecha_inicio": request.form.get("fecha_inicio", "").strip(),
        "fecha_fin": request.form.get("fecha_fin", "").strip(),
        "itinerario": request.form.get("itinerario", "").strip(),
        "organizador_id": session["user_id"],
    }
    if not Trip.validate(data):
        flash(
            "Revisa el destino y el itinerario (máximo 40 caracteres). "
            "El inicio no puede estar en el pasado y el fin debe ser "
            "igual o posterior al inicio.",
            "viaje",
        )
        return redirect(url_for("nuevo_viaje"))

    if not Trip.save(data):
        abort(500)
    return redirect(url_for("dashboard"))


@app.route("/ver/<int:trip_id>")
@app.route("/cine/<int:trip_id>")
def ver_viaje(trip_id):
    """Muestra los detalles del viaje y quiénes se han inscrito."""
    if "user_id" not in session:
        return redirect(url_for("index"))

    trip = Trip.get_by_id(trip_id)
    if not trip:
        return redirect(url_for("dashboard"))

    return render_template(
        "verpeli.html",
        viaje=trip,
        viajeros=get_travelers(trip_id),
        ya_inscrito=Trip.is_traveler(trip_id, session["user_id"]),
    )


@app.route("/editar/<int:trip_id>")
@app.route("/cine/editar/<int:trip_id>")
def editar_viaje(trip_id):
    """Permite editar solamente a quien organizó el viaje."""
    if "user_id" not in session:
        return redirect(url_for("index"))

    trip = Trip.get_by_id(trip_id)
    if not trip:
        return redirect(url_for("dashboard"))
    if trip.organizador_id != session["user_id"]:
        flash("Solo la persona organizadora puede editar este viaje.", "viaje")
        return redirect(url_for("dashboard"))

    return render_template("editarpeli.html", viaje=trip)


@app.route("/actualizar/<int:trip_id>", methods=["POST"])
@app.route("/cine/actualizar/<int:trip_id>", methods=["POST"])
def actualizar_viaje(trip_id):
    """Valida cambios y guarda solo si la persona actual es la organizadora."""
    if "user_id" not in session:
        return redirect(url_for("index"))

    trip = Trip.get_by_id(trip_id)
    if not trip or trip.organizador_id != session["user_id"]:
        return redirect(url_for("dashboard"))

    data = {
        "id": trip_id,
        "destino": request.form.get("destino", "").strip(),
        "fecha_inicio": request.form.get("fecha_inicio", "").strip(),
        "fecha_fin": request.form.get("fecha_fin", "").strip(),
        "itinerario": request.form.get("itinerario", "").strip(),
    }
    if not Trip.validate(data):
        flash(
            "Revisa el destino y el itinerario (máximo 40 caracteres). "
            "El inicio no puede estar en el pasado y el fin debe ser "
            "igual o posterior al inicio.",
            "viaje",
        )
        return redirect(url_for("editar_viaje", trip_id=trip_id))

    if not Trip.update(data):
        abort(500)
    return redirect(url_for("dashboard"))


@app.route("/borrar/<int:trip_id>", methods=["POST"])
@app.route("/cine/borrar/<int:trip_id>", methods=["POST"])
def borrar_viaje(trip_id):
    """Elimina el viaje y sus inscripciones únicamente por petición del organizador."""
    if "user_id" not in session:
        return redirect(url_for("index"))

    trip = Trip.get_by_id(trip_id)
    if not trip or trip.organizador_id != session["user_id"]:
        return redirect(url_for("dashboard"))

    if not Trip.delete(trip_id):
        abort(500)
    return redirect(url_for("dashboard"))
