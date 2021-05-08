from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
	username = StringField('Cédula de identidad', validators=[DataRequired()], render_kw={'placeholder': 'Ej. 12345678'})
	password = PasswordField('Contraseña', validators=[DataRequired()])
	remember_me = BooleanField('Recuerdame')
	submit = SubmitField('Inicia sesión')

class RegistrationForm(FlaskForm):
    username = StringField('Cédula de identidad', validators=[DataRequired()], render_kw={'placeholder': 'Ej. 12345678'})
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    password2 = PasswordField('Repite la contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Esa cédula de identidad ya está en uso.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Ese email ya está en uso.')

class ValidarTicket(FlaskForm):
    ticket = StringField('Código de ticket', validators = [DataRequired()])
    submit = SubmitField('Verificar')

class GenerarTicket(FlaskForm):
    submit = SubmitField('Generar')