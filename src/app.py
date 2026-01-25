"""Flask API som returnerer tall, kvadrat og versjon."""

from flask import Flask, jsonify

# Opprett et Flask-objekt
app = Flask(__name__)

APP_VERSION = "1.0"


# Knytt URL-en til funksjonen under
@app.get("/api/kvadrat/<int:tall>")
def kvadrat(tall):
    # Returner data som JSON
    return jsonify({"tall": tall, "kvadrat": tall * tall})


@app.get("/api/version")
def version():
    return jsonify({"version": APP_VERSION})


if __name__ == "__main__":
    # Start Flask-serveren
    # Lytt på alle nettverksgrensesnitt på port 5000
    app.run(host="0.0.0.0", port=5000)

# Smidig IT-2 © TIP AS, 2026
