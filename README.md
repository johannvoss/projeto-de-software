# Anjos da Noite — MVP

Projeto acadêmico de software web responsivo para registrar doações de alimentos e a produção/distribuição de marmitas da ONG fictícia Anjos da Noite.

## Ferramentas

Python, Flask, SQLite (previsto para próximas etapas), SQLAlchemy, Bootstrap e Pytest.

## Executar no Windows (PowerShell)

1. Instale Python 3.11 ou superior, Git e VS Code.
2. Abra um terminal PowerShell dentro da pasta deste projeto.
3. Rode:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

4. Abra http://127.0.0.1:5000 no navegador.

> A aplicação usa servidor de desenvolvimento e **não deve ser publicada assim** em produção.

## Testes

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Estado do MVP

- [x] Página inicial responsiva
- [x] Primeiro teste automatizado
- [ ] Autenticação de voluntários
- [ ] Banco SQLite
- [ ] Cadastro de doações
- [ ] Cadastro e histórico de marmitas
- [ ] Histórico de registros
- [ ] CI no GitHub Actions e Pull Request
- [ ] Validação com a comunidade (duas rodadas)

Não existem registros fictícios, credenciais reais ou arquivos de banco de dados no repositório.
