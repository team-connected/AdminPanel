from wtforms import StringField, SubmitField, SelectField
from flask_wtf import FlaskForm
import urllib.request
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
import os

class SearchForm(FlaskForm):
    type = SelectField('Categorie', choices=[('nurse', 'Medewerker'), ('patient', 'Patiënt'), ('metric', 'Meting'), ('device', 'Apparaat')])
    term = StringField('ID or S/N', [ DataRequired(message=('That\'s not a valid ID.'))])
    submit = SubmitField('Search')

class createPatient(FlaskForm):
    firstname = StringField('Voornaam', [ DataRequired(message=('You must provide this field!'))])
    lastname = StringField('Achternaam', [ DataRequired(message=('You must provide this field!'))])
    email = StringField('E-Mail', [ Length(min=6, message=(u'Little short for an email address?')), Email(message=('That\'s not a valid email address.')), DataRequired(message=('That\'s not a valid email address.'))])
    street = StringField('Adres', [ DataRequired(message=('You must provide this field!'))])
    city = StringField('Stad', [ DataRequired(message=('You must provide this field!'))])
    location = StringField('Locatie', [ DataRequired(message=('You must provide this field!'))])
    submit = SubmitField('Toevoegen')

class createMetric(FlaskForm):
    gewicht = StringField('Gewicht', [ DataRequired(message=('You must provide this field!'))])
    temperatuur = StringField('Temperatuur', [ DataRequired(message=('You must provide this field!'))])
    bloeddruk = StringField('Bloeddruk', [ DataRequired(message=('You must provide this field!'))])
    gewicht_device = StringField('Gewicht Apparaat', [ DataRequired(message=('You must provide this field!'))])
    temperatuur_device = StringField('Temperatuur Apparaat', [ DataRequired(message=('You must provide this field!'))])
    bloeddruk_device = StringField('Bloeddruk Apparaat', [ DataRequired(message=('You must provide this field!'))])
    pijnscore = StringField('Pijnscore', [ DataRequired(message=('You must provide this field!'))])
    nurse_id = StringField('Medewerker ID', [ DataRequired(message=('You must provide this field!'))])
    comment = StringField('Comment')
    submit = SubmitField('Toevoegen')