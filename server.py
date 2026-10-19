"""Punto de entrada: ejecuta la aplicación Flask en el puerto local 5000."""

from flask_app import app


if __name__ == "__main__":
    # El modo debug facilita el desarrollo local; desactívalo en producción.
    app.run(debug=True, port=5000)