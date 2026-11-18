"""Verifica se o monitor pode acessar o endpoint sem login."""
from test_app import app_teste, cliente


def test_endpoint_saude_publico(cliente):
    r = cliente.get('/saude')
    assert r.status_code == 200
    assert r.data == b'OK'


def test_rota_principal_permanece_protegida(cliente):
    r = cliente.get('/')
    assert r.status_code == 302
    assert '/entrar' in r.headers['Location']
