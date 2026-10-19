"""Configura la aplicación Flask y conecta sus extensiones principales."""

import os

from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
# La clave debe configurarse en el entorno al publicar la aplicación.
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "clave-local-para-desarrollo")

bcrypt = Bcrypt(app)

# Los controladores se importan aquí para registrar sus rutas al iniciar Flask.
from flask_app.controllers import usuarios, peliculas, comentarios