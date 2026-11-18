"""Aplicação inicial do MVP Anjos da Noite."""
from flask import Flask, render_template


def criar_app():
    app = Flask(__name__)

    @app.get("/")
    def inicio():
        return render_template("index.html")

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
