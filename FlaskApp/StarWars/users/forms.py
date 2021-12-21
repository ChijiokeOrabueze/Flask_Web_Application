from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from StarWars.Models import User




class RegisterationForm(FlaskForm):
    fullname = StringField("Fullname", validators = [DataRequired(), Length(min= 5, max= 30)])
    username = StringField("Username", validators=[DataRequired(), Length(min = 5, max = 20) ])
    email = StringField('Email', validators = [DataRequired(), Email() ])
    password = PasswordField("Password", validators = [DataRequired(), Length(min= 8, message="Weak password. Password should be at least 8 characters long.")])
    confirm_password = PasswordField("Confirm password", validators = [DataRequired(), EqualTo("password", message = "Passwords does not match.")])
    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('We already have an account with this email. Please use a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()]) 
    password = PasswordField('Password', validators = [DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class UpdateForm(FlaskForm):
    fullname = StringField("Fullname", validators = [DataRequired(), Length(min= 5, max= 30)])
    username = StringField("Username", validators=[DataRequired(), Length(min = 5, max = 20) ])
    email = StringField('Email', validators = [DataRequired(), Email() ])
    picture = FileField('Update Profile Picture', validators = [FileAllowed(['jpeg', 'jpg', 'png'])])
    submit = SubmitField("Update")


    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('We already have an account with this email. Please use a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    submit = SubmitField('Request password reset')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError('Sorry, this email does not exist on our database. Check and try again')

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators = [DataRequired(), Length(min= 8,
     message="Weak password. Password should be at least 8 characters long.")])
    confirm_password = PasswordField("Confirm password", validators = [DataRequired(), 
    EqualTo("password", message = "Passwords does not match.")])
    submit = SubmitField("Resest Password")
