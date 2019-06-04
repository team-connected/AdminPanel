from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
import urllib.request
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
import os

apiUrl = os.getenv("apiUrl", "http://192.168.0.163:5000")

class SearchForm(FlaskForm):
    email = StringField('E-Mail', [ Length(min=6, message=(u'Little short for an email address?')), Email(message=('That\'s not a valid email address.')), DataRequired(message=('That\'s not a valid email address.'))])
    submit = SubmitField('Search')
    
    #DEZE OPLOSSING GEEFT DE ERROR: TypeError: can only concatenate str (not "StringField") to str
    # def validate_email(self, email):
    #     """Email validation."""
    #     #API URL TO CHECK USER: http://192.168.0.163:5000/api/v1/users/email=jbakkers@outlook.com
    #     user = urllib.request.urlopen(apiUrl+'/api/v1/users/email='+str(emailCheck))
    #     if user.getcode() == 404:
    #         raise ValidationError('Please use a different email address.')