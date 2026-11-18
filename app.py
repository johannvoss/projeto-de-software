"""Aplicação Flask do MVP Anjos da Noite — autenticação e banco SQLite."""
import os
import re
import secrets
from datetime import timedelta
from pathlib import Path

import click
from flask import Flask, abort, flash, redirect, render_template, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from forms import FormLogin, FormSair
from models import Base, Voluntario, agora_utc


BLOQUEIO_MINUTOS = 15
LIMITE_TENTATIVAS = 5


def criar_app(configuracao=None):
    app = Flask(__name__)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    # Em ambiente local, uma chave é gerada a cada inicialização.
    # Para hospedar futuramente, defina SECRET_KEY fixa no ambiente.
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY") or secrets.token_hex(32),
        DATABASE_URL=os.getenv("DATABASE_URL") or
                     f"sqlite:///{(Path(app.instance_path) / 'database.db').as_posix()}",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.getenv("COOKIE_SECURE") == "1",
    )
    if configuracao:
        app.config.update(configuracao)

    engine = create_engine(app.config["DATABASE_URL"])
    Base.metadata.create_all(engine)
    fabrica_sessoes = sessionmaker(bind=engine, expire_on_commit=False)
    app.extensions["fabrica_sessoes"] = fabrica_sessoes
    app.extensions["motor_sqlite"] = engine

    login_manager = LoginManager()
    login_manager.login_view = "entrar"
    login_manager.login_message = "Entre com seu e-mail e senha para continuar."
    login_manager.init_app(app)

    @login_manager.user_loader
    def carregar_usuario(identificador):
        try:
            numero = int(identificador)
        except (TypeError, ValueError):
            return None
        with fabrica_sessoes() as sessao:
            return sessao.get(Voluntario, numero)

    @app.get("/")
    @login_required
    def inicio():
        return render_template("index.html", form_sair=FormSair())

    @app.route("/entrar", methods=["GET", "POST"])
    def entrar():
        if current_user.is_authenticated:
            return redirect(url_for("inicio"))

        form = FormLogin()
        if form.validate_on_submit():
            email = form.email.data.strip().lower()
            senha = form.senha.data
            agora = agora_utc()

            with fabrica_sessoes() as sessao:
                voluntario = sessao.scalar(select(Voluntario).where(Voluntario.email == email))
                if voluntario and voluntario.bloqueado_ate and voluntario.bloqueado_ate > agora:
                    flash("Acesso temporariamente bloqueado. Tente novamente em 15 minutos.", "warning")
                elif voluntario and check_password_hash(voluntario.senha_hash, senha):
                    voluntario.tentativas_falhas = 0
                    voluntario.bloqueado_ate = None
                    sessao.commit()
                    login_user(voluntario)
                    return redirect(url_for("inicio"))
                else:
                    if voluntario:
                        # Se o tempo de bloqueio já terminou, reinicia o contador.
                        if voluntario.bloqueado_ate and voluntario.bloqueado_ate <= agora:
                            voluntario.tentativas_falhas = 0
                            voluntario.bloqueado_ate = None
                        voluntario.tentativas_falhas += 1
                        if voluntario.tentativas_falhas >= LIMITE_TENTATIVAS:
                            voluntario.bloqueado_ate = agora + timedelta(minutes=BLOQUEIO_MINUTOS)
                        sessao.commit()
                    flash("E-mail ou senha inválidos.", "danger")

        return render_template("login.html", form=form)

    @app.post("/sair")
    @login_required
    def sair():
        formulario = FormSair()
        if not formulario.validate_on_submit():
            abort(400)
        logout_user()
        flash("Você saiu do sistema.", "success")
        return redirect(url_for("entrar"))

    @app.cli.command("criar-voluntario")
    @click.option("--email", prompt="E-mail do voluntário")
    def criar_voluntario(email):
        """Cria uma conta autorizada no terminal (sem cadastro público)."""
        email = email.strip().lower()
        if len(email) > 254 or not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", email):
            raise click.ClickException("E-mail inválido.")
        senha = click.prompt("Senha (mínimo 8 caracteres)", hide_input=True, confirmation_prompt=True)
        if len(senha) < 8:
            raise click.ClickException("A senha deve ter pelo menos 8 caracteres.")
        with fabrica_sessoes() as sessao:
            existente = sessao.scalar(select(Voluntario).where(Voluntario.email == email))
            if existente:
                raise click.ClickException("Já existe um voluntário com esse e-mail.")
            sessao.add(Voluntario(
                email=email,
                senha_hash=generate_password_hash(senha, method="pbkdf2:sha256", salt_length=16),
            ))
            sessao.commit()
        click.echo("Voluntário cadastrado com sucesso!")

    return app


app = criar_app()

if __name__ == "__main__":
    app.run(debug=True)
