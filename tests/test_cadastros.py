from sqlalchemy import select
from models import Doacao, Marmita
from forms import hoje_sp
from test_app import app_teste, cliente  # mesmos fixtures da etapa 2


def login(cliente):
    return cliente.post('/entrar', data={'email': 'teste@exemplo.com', 'senha': 'senha-forte-de-teste'})


def test_cadastros_exigem_login(cliente):
    assert cliente.get('/doacoes/nova').status_code == 302
    assert cliente.get('/marmitas/nova').status_code == 302


def test_registra_doacao_e_exibe_no_painel(cliente, app_teste):
    login(cliente)
    r = cliente.post('/doacoes/nova', data={'alimento':'Arroz', 'quantidade':'2.50', 'unidade':'kg', 'data':hoje_sp().isoformat()}, follow_redirects=True)
    assert r.status_code == 200
    assert b'Arroz' in r.data
    with app_teste.extensions['fabrica_sessoes']() as s:
        assert s.scalar(select(Doacao)).unidade == 'kg'


def test_impede_doacao_zero(cliente, app_teste):
    login(cliente)
    r = cliente.post('/doacoes/nova', data={'alimento':'Arroz', 'quantidade':'0', 'unidade':'kg', 'data':hoje_sp().isoformat()})
    assert r.status_code == 200
    with app_teste.extensions['fabrica_sessoes']() as s:
        assert s.scalar(select(Doacao)) is None


def test_registra_marmitas_e_atualiza_resumo(cliente, app_teste):
    login(cliente)
    r = cliente.post('/marmitas/nova', data={'produzida':'30', 'distribuida':'20', 'data':hoje_sp().isoformat()}, follow_redirects=True)
    assert r.status_code == 200
    assert b'30' in r.data and b'20' in r.data
    with app_teste.extensions['fabrica_sessoes']() as s:
        assert s.scalar(select(Marmita)).quantidade_distribuida == 20


def test_impede_distribuida_maior_que_produzida(cliente, app_teste):
    login(cliente)
    r = cliente.post('/marmitas/nova', data={'produzida':'10', 'distribuida':'11', 'data':hoje_sp().isoformat()})
    assert r.status_code == 200
    with app_teste.extensions['fabrica_sessoes']() as s:
        assert s.scalar(select(Marmita)) is None
