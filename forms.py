from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class CharacterForm(FlaskForm):
    name = StringField('Character Name', validators=[DataRequired(), Length(min=1, max=150)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0, max=500)])
    appearance = TextAreaField('Appearance', validators=[DataRequired()])
    personality = TextAreaField('Personality', validators=[DataRequired()])
    backstory = TextAreaField('Backstory', validators=[DataRequired()])
    universe = SelectField('Universe', coerce=int, validators=[DataRequired()])
    image = FileField('Character Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
