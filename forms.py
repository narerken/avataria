from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from flask_wtf.file import FileAllowed

# Form for user login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired()])

# Form for user registration
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])  # Password match check is handled in route

# Form for creating or editing a character
class CharacterForm(FlaskForm):
    name = StringField('Character Name', validators=[DataRequired(), Length(min=1, max=150)])
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0, max=500)])
    appearance = TextAreaField('Appearance', validators=[DataRequired()])
    personality = TextAreaField('Personality', validators=[DataRequired()])
    backstory = TextAreaField('Backstory', validators=[DataRequired()])
    universe = SelectField('Universe', coerce=int, validators=[DataRequired()])  # Choices set in view
    image = FileField('Character Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
