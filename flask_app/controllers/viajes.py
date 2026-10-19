from datetime import date

from flask import abort, flash, redirect, render_template, request, session, url_for

from flask_app import app
from flask_app.models.viajes import Trip
from flask_app.models.usuarios import User


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("index"))

    user = User.get_by_id(session["user_id"])
    if not user:
        session.clear()
        return redirect(url_for("index"))

    return render_template("dashboard.html", viajes=Trip.get_all())


@app.route("/nuevo")
def nuevo_viaje():
    if "user_id" not in session:
        return redirect(url_for("index"))
    return render_template("nuevo.html", hoy=date.today().isoformat())


@app.route("/crear", methods=["POST"])
def crear_viaje():
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
            "posterior al inicio.",
            "viaje",
        )
        return redirect(url_for("nuevo_viaje"))

    if not Trip.save(data):
        abort(500)
    return redirect(url_for("dashboard"))


@app.route("/ver/<int:trip_id>")
def ver_viaje(trip_id):
    if "user_id" not in session:
        return redirect(url_for("index"))

    trip = Trip.get_by_id(trip_id)
    if not trip:
        return redirect(url_for("dashboard"))

    return render_template(
        "ver.html",
        viaje=trip,
        viajeros=Trip.get_travelers(trip_id),
        ya_inscrito=Trip.is_traveler(trip_id, session["user_id"]),
    )


@app.route("/editar/<int:trip_id>")
def editar_viaje(trip_id):
    if "user_id" not in session:
        return redirect(url_for("index"))

    trip = Trip.get_by_id(trip_id)
    if not trip:
        return redirect(url_for("dashboard"))
    # solo quien organizó el viaje puede editarlo
    if trip.organizador_id != session["user_id"]:
        flash("Solo la persona organizadora puede editar este viaje.", "viaje")
        return redirect(url_for("dashboard"))

    return render_template("editar.html", viaje=trip, hoy=date.today().isoformat())


@app.route("/actualizar/<int:trip_id>", methods=["POST"])
def actualizar_viaje(trip_id):
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
            "posterior al inicio.",
            "viaje",
        )
        return redirect(url_for("editar_viaje", trip_id=trip_id))

    if not Trip.update(data):
        abort(500)
    return redirect(url_for("dashboard"))


@app.route("/borrar/<int:trip_id>", methods=["POST"])
def borrar_viaje(trip_id):
    if "user_id" not in session:
        return redirect(url_for("index"))

    trip = Trip.get_by_id(trip_id)
    if not trip or trip.organizador_id != session["user_id"]:
        return redirect(url_for("dashboard"))

    if not Trip.delete(trip_id):
        abort(500)
    return redirect(url_for("dashboard"))
