from flask_wtf import FlaskForm
from wtforms import EmailField,MultipleFileField,StringField, PasswordField, SubmitField,IntegerField
from wtforms.validators import  DataRequired,Length,EqualTo,NumberRange,Email
from flask_wtf.file import FileField, FileRequired, FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('password_confirm', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')


class adminRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('password_confirm', validators=[DataRequired(),EqualTo('password')])
    adminkey = StringField('adminkey',validators=[DataRequired()])
    submit = SubmitField('Register')


class Loginform(FlaskForm):
    username= StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('login')

class PropertyForm(FlaskForm):
    contact_email = EmailField('contact_email', validators=[DataRequired(), Email(), Length(max=100)])
    contact_number = StringField('contact_number', validators=[DataRequired(), Length(min=10, max=10)])
    location = StringField('location', validators=[DataRequired(), Length(max=100)])
    price = IntegerField('price', validators=[DataRequired(), NumberRange(min=1)])
    bedrooms = IntegerField('bedrooms', validators=[DataRequired(), NumberRange(min=1)])
    bathrooms = IntegerField('bathrooms', validators=[DataRequired(), NumberRange(min=1)])
    carpet_area = IntegerField('carpet_area', validators=[DataRequired(), NumberRange(min=1)])
    images = MultipleFileField('upload_image',validators=[FileAllowed(['jpg','png','jpeg'],'Images only')])
    submit = SubmitField('Create Property')