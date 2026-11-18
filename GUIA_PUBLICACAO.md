# Publicação do MVP Anjos da Noite — PythonAnywhere

Este pacote altera somente `app.py`, `requirements.txt` e adiciona `tests/test_monitoramento.py`.
Ele **não inclui o banco de dados**, usuários, senhas ou chaves.

## 1. Aplicar no projeto que está funcionando

1. Faça backup do projeto, em especial `instance/database.db`.
2. Copie `app.py` e `requirements.txt` sobre os arquivos equivalentes do seu projeto.
3. Copie `tests/test_monitoramento.py` para a pasta `tests/` do seu projeto.
4. Não apague nem substitua `instance/`.
5. Na raiz do projeto, rode `python -m pip install -r requirements.txt` e `python -m pytest -q`.
6. Confira se `.gitignore` contém `instance/`, `.env`, `*.db`, `.venv/`.
7. Faça um commit real das alterações: `git add app.py requirements.txt tests/test_monitoramento.py` e `git commit -m "chore: preparar deploy e monitoramento"`.
8. Publique o repositório no GitHub e envie o commit (`git push`).

## 2. Criar hospedagem gratuita

1. Cadastre-se em https://www.pythonanywhere.com/ .
2. Na aba **Consoles**, abra **Bash**.
3. Na aba Bash, clone seu repositório público (ajuste URL):

```bash
git clone https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git anjos-da-noite
cd ~/anjos-da-noite
python3.13 -m venv ~/.virtualenvs/anjos-env
~/.virtualenvs/anjos-env/bin/python -m pip install -r requirements.txt
```

4. Cadastre seu primeiro voluntário (use uma senha exclusiva para demonstração):

```bash
~/.virtualenvs/anjos-env/bin/python -m flask --app app criar-voluntario
```

5. Na aba **Web**, clique em **Add a new web app** > **Manual configuration** > Python 3.13 (ou use a mesma versão do venv).
6. Na seção **Virtualenv**, configure `/home/SEU-USUARIO/.virtualenvs/anjos-env`.
7. Abra o arquivo WSGI exibido na aba Web e substitua seu conteúdo, ajustando usuário e a chave gerada:

```python
import os
import sys

os.environ['SECRET_KEY'] = 'COLE_AQUI_UMA_CHAVE_ALEATORIA_LONGA_E_EXCLUSIVA'
os.environ['COOKIE_SECURE'] = '1'
path = '/home/SEU-USUARIO/anjos-da-noite'
if path not in sys.path:
    sys.path.insert(0, path)
from app import app as application
```

Crie a chave no console Bash com:

```bash
python3.13 -c "import secrets; print(secrets.token_hex(32))"
```

Coloque a chave **somente no WSGI**, que não deve estar no seu repositório GitHub. Não compartilhe essa chave em prints.

8. Opcional: configure em **Static files** o URL `/static/` para `/home/SEU-USUARIO/anjos-da-noite/static/`.
9. Pressione **Reload** na aba Web.
10. Teste `https://SEU-USUARIO.pythonanywhere.com/saude` (deve mostrar `OK`), depois abra `/entrar` para conferir a interface.

## 3. Monitorar indisponibilidade

1. Crie conta em https://uptimerobot.com/.
2. Escolha **Add New Monitor** > **HTTP(s)**.
3. URL: `https://SEU-USUARIO.pythonanywhere.com/saude`.
4. Frequência: 5 minutos no plano gratuito, selecione alerta por e-mail.
5. Faça captura da página do aplicativo e do monitor exibindo "Up" após o teste.

## 4. Cuidados importantes

- A URL localhost `127.0.0.1` não serve para entrega. Você precisa publicar e usar o endereço real do PythonAnywhere.
- No plano gratuito do PythonAnywhere, o app tem vencimento mensal; verifique e renove antes da avaliação.
- O banco SQLite fica na pasta `instance` **da hospedagem** e permanece nesse sistema de arquivos. Faça backups regulares.
- Não envie `database.db` ou arquivos de instância ao GitHub. O professor precisará de credenciais de teste enviadas em canal privado, caso queira usar os cadastros.
- Monitoramento de `/saude` confirma a resposta HTTP e a consulta básica ao banco, mas não substitui testes de login e cadastros.
- Não use o servidor Flask `python app.py` para publicar na internet; o PythonAnywhere carrega `app` via WSGI.
- Se a URL falhar, consulte as seções **Error log** e **Server log** na aba Web.
