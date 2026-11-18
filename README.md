# ONG Anjos da Noite — MVP (Etapa 3)

Sistema acadêmico simples para gestão de doações e distribuição de marmitas. Desenvolvido com Flask, SQLAlchemy, SQLite, Bootstrap e Pytest.

## Atualizar sem perder seu usuário

1. Faça uma cópia de segurança do arquivo `instance/database.db` da versão anterior.
2. Copie os arquivos deste pacote para a **mesma pasta `anjos-da-noite`** usada anteriormente, sobrescrevendo os arquivos de código.
3. **Não substitua nem apague `instance/` e `.venv/`.** Não copie o banco de dados de outro projeto.
4. Execute, na pasta `anjos-da-noite`, com o ambiente virtual ativado:

```powershell
python -m pip install -r requirements.txt
python app.py
```

Acesse http://127.0.0.1:5000 e entre com o mesmo e-mail e senha da etapa anterior.

## Criar um novo voluntário (somente se necessário)

```powershell
python -m flask --app app criar-voluntario
```

## Testar

```powershell
python -m pytest -q
```

## Funcionalidades

- Login de voluntário autorizado e saída segura.
- Dashboard com totais diários.
- Cadastro de doações de alimentos (quantidade e unidade).
- Cadastro de marmitas produzidas e distribuídas.
- Histórico recente ordenado por data.
- Validação no servidor e token CSRF nos formulários.

## Limites

- Projeto local/de demonstração. Não exponha o servidor Flask diretamente na internet.
- Sem edição e exclusão de registros nesta versão.
- O limite de tempo de carregamento e WCAG AA precisam ser avaliados em testes com usuários/dispositivos reais.
- O banco `instance/database.db` está ignorado no Git por segurança. Nunca publique senhas ou segredos.
