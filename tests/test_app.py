from datetime import timedelta

import pytest
from sqlalchemy import inspect, select
from werkzeug.security import generate_password_hash

from app import criar_app
from models import Voluntario, agora_utc


@pytest.fixture
def app_teste(tmp_path):
    app = criar_app({
        "TESTING": True,
        "SECRET_KEY": "chave-de-teste-local-123456",
        "DATABASE_URL": f"sqlite:///{(tmp_path / 'teste.db').as_posix()}",
        "WTF_CSRF_ENABLED": False,  # Simplifica somente os testes automatizados.
    })
    with app.extensions["fabrica_sessoes"]() as sessao:
        sessao.add(Voluntario(
            email="teste@exemplo.com",
            senha_hash=generate_password_hash("senha-forte-de-teste", method="pbkdf2:sha256"),
        ))
        sessao.commit()
    yield app
    app.extensions["motor_sqlite"].dispose()


@pytest.fixture
def cliente(app_teste):
    return app_teste.test_client()


def test_banco_gera_tabelas(app_teste):
    nomes = inspect(app_teste.extensions["motor_sqlite"]).get_table_names()
    assert {"voluntarios", "doacoes", "marmitas"}.issubset(nomes)


def test_pagina_inicial_exige_login(cliente):
    resposta = cliente.get("/")
    assert resposta.status_code == 302
    assert "/entrar" in resposta.headers["Location"]


def test_tela_de_login_carrega(cliente):
    resposta = cliente.get("/entrar")
    assert resposta.status_code == 200
    assert b"Anjos da Noite" in resposta.data


def test_login_invalido_nao_entra(cliente):
    resposta = cliente.post("/entrar", data={
        "email": "teste@exemplo.com", "senha": "errada"
    }, follow_redirects=True)
    assert b"inv" in resposta.data
    assert b"Acesso dos volunt" in resposta.data


def test_login_e_logout(cliente):
    resposta = cliente.post("/entrar", data={
        "email": "teste@exemplo.com", "senha": "senha-forte-de-teste"
    }, follow_redirects=True)
    assert resposta.status_code == 200
    assert b"Painel do dia" in resposta.data
    assert b"teste@exemplo.com" in resposta.data

    resposta = cliente.post("/sair", follow_redirects=True)
    assert resposta.status_code == 200
    assert b"Acesso dos volunt" in resposta.data
    assert cliente.get("/").status_code == 302


def test_bloqueia_apos_cinco_tentativas(cliente, app_teste):
    for _ in range(5):
        cliente.post("/entrar", data={
            "email": "teste@exemplo.com", "senha": "errada"
        })
    with app_teste.extensions["fabrica_sessoes"]() as sessao:
        voluntario = sessao.scalar(select(Voluntario).where(Voluntario.email == "teste@exemplo.com"))
        assert voluntario.tentativas_falhas == 5
        assert voluntario.bloqueado_ate is not None
        assert voluntario.bloqueado_ate > agora_utc()

    # Nem uma senha correta deve entrar enquanto o bloqueio estiver ativo.
    resposta = cliente.post("/entrar", data={
        "email": "teste@exemplo.com", "senha": "senha-forte-de-teste"
    }, follow_redirects=True)
    assert b"temporariamente bloqueado" in resposta.data
    assert cliente.get("/").status_code == 302


def test_bloqueio_expirado_permite_login(cliente, app_teste):
    with app_teste.extensions["fabrica_sessoes"]() as sessao:
        voluntario = sessao.scalar(select(Voluntario).where(Voluntario.email == "teste@exemplo.com"))
        voluntario.tentativas_falhas = 5
        voluntario.bloqueado_ate = agora_utc() - timedelta(minutes=1)
        sessao.commit()
    resposta = cliente.post("/entrar", data={
        "email": "teste@exemplo.com", "senha": "senha-forte-de-teste"
    }, follow_redirects=True)
    assert b"Painel do dia" in resposta.data
