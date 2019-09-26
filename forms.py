from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.fields.html5 import EmailField 
from wtforms.validators import InputRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[InputRequired('Enter Email')])
    password = PasswordField("Password", validators=[InputRequired('Enter Password')])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[InputRequired("Please enter a valid email address")])
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])
    #confirm = PasswordField("Confirm Password")
    submit = SubmitField("Register")


