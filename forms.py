"""Formulários com proteção CSRF."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp


class FormLogin(FlaskForm):
    email = StringField(
        "E-mail", validators=[DataRequired(), Length(max=254),
                               Regexp(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", message="Informe um e-mail válido.")]
    )
    senha = PasswordField("Senha", validators=[DataRequired()])
    entrar = SubmitField("Entrar")


class FormSair(FlaskForm):
    sair = SubmitField("Sair")
