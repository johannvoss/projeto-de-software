"""Formulários do MVP com validação no servidor e proteção CSRF."""
from datetime import datetime
from zoneinfo import ZoneInfo

from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, IntegerField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, InputRequired, Length, NumberRange, Regexp, ValidationError


def hoje_sp():
    return datetime.now(ZoneInfo('America/Sao_Paulo')).date()


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Length(max=254),
        Regexp(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', message='Informe um e-mail válido.')])
    senha = PasswordField('Senha', validators=[DataRequired()])
    entrar = SubmitField('Entrar')


class FormSair(FlaskForm):
    sair = SubmitField('Sair')


class FormDoacao(FlaskForm):
    alimento = StringField('Nome do alimento', validators=[DataRequired(message='Informe o alimento.'), Length(max=120)])
    quantidade = DecimalField('Quantidade', places=2, validators=[InputRequired(message='Informe a quantidade.'), NumberRange(min=0.01, message='A quantidade deve ser maior que zero.')])
    unidade = SelectField('Unidade', choices=[('kg', 'Quilogramas (kg)'), ('un', 'Unidades'), ('litros', 'Litros')], validators=[DataRequired()])
    data = DateField('Data da doação', format='%Y-%m-%d', default=hoje_sp, validators=[InputRequired(message='Informe a data.')])
    salvar = SubmitField('Salvar doação')

    def validate_data(self, campo):
        if campo.data > hoje_sp():
            raise ValidationError('A data não pode estar no futuro.')


class FormMarmita(FlaskForm):
    produzida = IntegerField('Quantidade produzida', validators=[InputRequired(message='Informe a quantidade produzida.'), NumberRange(min=1, message='Informe pelo menos uma marmita.')])
    distribuida = IntegerField('Quantidade distribuída', validators=[InputRequired(message='Informe a quantidade distribuída.'), NumberRange(min=0, message='A quantidade não pode ser negativa.')])
    data = DateField('Data do registro', format='%Y-%m-%d', default=hoje_sp, validators=[InputRequired(message='Informe a data.')])
    salvar = SubmitField('Salvar registro')

    def validate_distribuida(self, campo):
        if self.produzida.data is not None and campo.data is not None and campo.data > self.produzida.data:
            raise ValidationError('O total distribuído não pode superar o produzido.')

    def validate_data(self, campo):
        if campo.data > hoje_sp():
            raise ValidationError('A data não pode estar no futuro.')
