from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    # si ya inicio sesion lo mando directo al dashboard
    if 'usuario_id' in session:
        return redirect('/dashboard')
    return render_template('inicio_sesion.html')

@app.route('/registro', methods=['POST'])
def registro():
    if not Usuario.validar_registro(request.form):
        return redirect('/')

    pass_hasheado = bcrypt.generate_password_hash(request.form['password'])

    datos = {
        'nombre': request.form['nombre'],
        'apellido': request.form['apellido'],
        'email': request.form['email'],
        'password': pass_hasheado
    }
    nuevo_id = Usuario.save(datos)

    session['usuario_id'] = nuevo_id
    session['nombre'] = request.form['nombre']
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    usuario = Usuario.get_by_email({'email': request.form['email']})

    if not usuario:
        flash("El e-mail no está registrado", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(usuario.password, request.form['password']):
        flash("Contraseña incorrecta", "login")
        return redirect('/')

    session['usuario_id'] = usuario.id
    session['nombre'] = usuario.nombre
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
