from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm( FlaskForm ):
    email = StringField( "email" , validators = [ DataRequired() , Email()])
    password = PasswordField( "Contraseña" , validators = [ DataRequired() ] )
    remember_me = BooleanField( "Recuerdame" )
    submit = SubmitField( "Ingresar" )

class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    rol = StringField('Rol', validators=[DataRequired()])
    submit = SubmitField('Registrar')