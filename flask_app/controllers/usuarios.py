from flask import abort, flash, redirect, render_template, request, session, url_for

from flask_app import app, bcrypt
from flask_app.models.usuarios import User


@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/registro", methods=["POST"])
def register():
    if not User.validate_register(request.form):
        flash(
            "Revisa los datos: nombre y apellido de al menos 2 caracteres, "
            "correo válido y contraseñas iguales.",
            "registro",
        )
        return redirect(url_for("index"))

    data = {
        "nombre": request.form["nombre"].strip(),
        "apellido": request.form["apellido"].strip(),
        "email": request.form["email"].strip().lower(),
        "password": bcrypt.generate_password_hash(request.form["password"]).decode("utf-8"),
    }
    user_id = User.save(data)
    if not user_id:
        abort(500)

    session["user_id"] = user_id
    session["user_name"] = data["nombre"]
    return redirect(url_for("dashboard"))


@app.route("/login", methods=["POST"])
def login():
    valid, user = User.validate_login(request.form)
    if not valid or not bcrypt.check_password_hash(user.password, request.form.get("password", "")):
        flash("El correo o la contraseña son incorrectos.", "login")
        return redirect(url_for("index"))

    session["user_id"] = user.id
    session["user_name"] = user.nombre
    return redirect(url_for("dashboard"))


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))
