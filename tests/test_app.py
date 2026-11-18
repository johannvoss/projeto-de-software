from app import criar_app


def test_pagina_inicial_carrega():
    app = criar_app()
    app.config["TESTING"] = True

    with app.test_client() as cliente:
        resposta = cliente.get("/")

    assert resposta.status_code == 200
    assert b"Anjos da Noite" in resposta.data
