from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms.fields.simple import HiddenField

class RegistrationForm(FlaskForm):
    access_key = StringField('access_key',
                           validators=[DataRequired(), Length(min=2, max=20)])
    secret_key = StringField('secret_key',
                        validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):

    access_key = StringField('access_key',
                           validators=[DataRequired(), Length(min=2, max=20)])
    secret_key = StringField('secret_key',
                        validators=[DataRequired()])
    submit = SubmitField('Login')



class RedirectToFolder(FlaskForm):
    bucket_name = HiddenField('bucket_name')
    submit = SubmitField('Open')


class CreateFolderForm(FlaskForm):
    bucket_name = HiddenField('bucket_name')
    folder_name = StringField('folder_name',validators=[DataRequired()])
    submit = SubmitField('Create')

class RenameFileForm(FlaskForm):
    old_name = HiddenField('old_name')
    bucket_name = HiddenField('bucket_name')
    folder_name = HiddenField('folder_name')
    new_name = StringField('new_name')
    submit = SubmitField('Rename')
