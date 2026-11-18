# Anjos da Noite — MVP

Sistema web acadêmico responsivo para registro de doações e controle da produção/distribuição de marmitas de uma ONG fictícia. Interface pensada para voluntários que utilizam celular.

## Tecnologias

Python, Flask, SQLAlchemy, SQLite, Flask-Login, Flask-WTF (CSRF), Bootstrap e Pytest.

## Instalação no Windows (PowerShell)

Este pacote pode ser extraído por cima da pasta `anjos-da-noite` da etapa 1. O `.venv` que você já criou fica fora dessa pasta e pode ser reaproveitado.

Abra o terminal **dentro** de `anjos-da-noite` e execute:

```powershell
..\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Cadastrar o primeiro voluntário (uma vez)

```powershell
..\.venv\Scripts\python.exe -m flask --app app criar-voluntario
```

Informe um e-mail e escolha uma senha de pelo menos 8 caracteres. A senha não aparece enquanto é digitada.

## Executar

```powershell
..\.venv\Scripts\python.exe app.py
```

Abra: http://127.0.0.1:5000

- Sem login, você será redirecionado para `/entrar`.
- Após entrar, verá a página inicial que já existia.
- Use **Sair** para encerrar a sessão.
- Após cinco tentativas incorretas seguidas para a mesma conta, ela fica bloqueada por quinze minutos.

## Banco de dados

O banco local é criado automaticamente em `instance/database.db` quando a aplicação inicia. Contém as tabelas `voluntarios`, `doacoes` e `marmitas`. Os dois cadastros e o histórico ainda serão implementados nas próximas etapas.

**Não envie** o arquivo `database.db` nem a pasta `.venv` ao GitHub (já estão no `.gitignore`). Para preservar registros locais, faça backup do `database.db` com o sistema fechado.

## Testes

```powershell
..\.venv\Scripts\python.exe -m pytest -q
```

## Segurança e publicação

- Cadastro de contas somente pelo terminal, não existe formulário de cadastro público.
- Hash de senha PBKDF2-SHA256 com salt aleatório.
- Formulários com CSRF, cookie HttpOnly e SameSite=Lax.
- Em ambiente local o cookie não usa `Secure` para permitir HTTP em `localhost`.
- **Não publique esta versão diretamente na internet:** para produção, configure HTTPS, `SECRET_KEY` permanente e `COOKIE_SECURE=1`, desative `debug` e use servidor WSGI adequado.
- O sistema não coleta dados pessoais dos destinatários de marmitas.

## Histórico do desenvolvimento

- [x] Página inicial responsiva.
- [x] Banco SQLite e modelagem de Voluntário, Doação e Marmita.
- [x] Login, logout e bloqueio temporário após cinco erros.
- [x] Testes de autenticação e criação de tabelas (devem ser executados pelo aluno).
- [ ] Formulários de cadastro de doações e marmitas.
- [ ] Histórico atualizado.
- [ ] GitHub Actions, commits e Pull Request.
- [ ] Duas rodadas de validação real com a comunidade.
