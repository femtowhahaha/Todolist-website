from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, HiddenField
from wtforms.validators import Length, EqualTo, DataRequired

class AddListForm(FlaskForm):

    description = StringField(label='Description', validators=[Length(min=0, max=200), DataRequired()])
    submit = SubmitField(label='Add')

class DeleteListForm(FlaskForm):
    todo_id = HiddenField(validators=[DataRequired()])
    delete = SubmitField(label='Delete')

class RegisterForm(FlaskForm):

    username = StringField(label="Username", validators=[Length(min=4, max=30), DataRequired()])
    password1 = PasswordField(label="Password", validators=[Length(min=4, max=50), DataRequired()])
    password2 = PasswordField(label="Confirm Password", validators=[Length(min=4, max=50), DataRequired(), EqualTo("password1")])
    register = SubmitField(label="Register")

class LoginForm(FlaskForm):

    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[ DataRequired()])
    login = SubmitField(label="Login")

class LogoutForm(FlaskForm):

    cancel = SubmitField("Cancel")
    logout = SubmitField("Log out")