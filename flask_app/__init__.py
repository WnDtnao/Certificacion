import os

from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "clave-local-para-desarrollo")

bcrypt = Bcrypt(app)

from flask_app.controllers import usuarios, viajes, viajeros