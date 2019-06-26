#!/usr/bin/env python3

from flask import Flask, render_template, redirect, url_for, session, g, current_app, request
#from flask_oidc import OpenIDConnect
from forms import SearchForm, createPatient, createMetric
import datetime
import requests
import urllib.request
import json
import unicodedata
import os
import pyfiglet

SECRET_KEY = os.urandom(32)

#ENV Flags
apiUrl = os.getenv("api_url", "http://umc-api.maartenmol.nl:5000")

#Print some usefull information to console
ascii_banner = pyfiglet.figlet_format("UMC AdminPanel")
print(ascii_banner)
print("Starting AdminPanel")
print("API Server Version: V1.0")
print("Developed by: Haydn Felida, Jeroen Verkerk, Sam Zandee, Shaniah Arrias, Maarten Mol. (All rights reserved)")

#Define APP
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
 
 
@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403
 
 
@app.errorhandler(410)
def page_not_found(e):
    return render_template('410.html'), 410

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/patienten")
def patienten():
    data = urllib.request.urlopen(apiUrl+'/api/v1/patient/')
    data = json.loads(data.read())

    return render_template("patienten.html", data=data)

@app.route("/verpleging")
def nurses():
    data = urllib.request.urlopen(apiUrl+'/api/v1/nurse/')
    data = json.loads(data.read())

    return render_template("nurses.html", data=data)

@app.route("/apparaten")
def apparaten():
    data = urllib.request.urlopen(apiUrl+'/api/v1/device/')
    data = json.loads(data.read())

    return render_template("devices.html", data=data)

@app.route("/showpatient=<id>")
def patient(id):
    data = urllib.request.urlopen(apiUrl+'/api/v1/patient/_id='+id)
    data = json.loads(data.read())[0]

    info = urllib.request.urlopen(apiUrl+'/api/v1/metric/patient='+id)
    if info.getcode() == 200:
        info = json.loads(info.read())
        return render_template("patient.html", data=data, metrics=info)
    
    else:
        return render_template("patient.html", data=data)    

@app.route("/shownurse=<id>")
def nurse(id):
    data = urllib.request.urlopen(apiUrl+'/api/v1/nurse/_id='+id)
    data = json.loads(data.read())[0]

    return render_template("nurse.html", data=data)

@app.route('/removemetric=<id>&patient=<pid>')
def removeMetric(pid,id):
    request = urllib.request.Request(apiUrl+'/api/v1/metric/patient='+pid+'/id='+id, method='DELETE')
    urllib.request.urlopen(request)
    return redirect('/showpatient=' + pid)

@app.route('/addmetric=<id>', methods=['GET', 'POST'])
def addmetric(id):
    form = createMetric()
    if form.validate_on_submit():

        cTime = str(datetime.datetime.now())

        datax = {'gewicht' : form.gewicht.data, 'bloeddruk' : form.bloeddruk.data, 'temperatuur' : form.temperatuur.data, 
                    'device_id' : form.device_id.data, 'nurse_id' : form.nurse_id.data, 'comment' : form.comment.data, 'timestamp' : cTime}
        data = json.dumps(datax, sort_keys=True, indent=4)
        r = requests.post(url = apiUrl + '/api/v1/metric/patient=' + id, data = data)

        response = json.loads(r.text)

        return redirect('/showpatient=' + id)

    return render_template('addmetric.html', form=form)

@app.route('/addpatient', methods=['GET', 'POST'])
def addpatient():
    form = createPatient()
    if form.validate_on_submit():
        datax = {'firstname' : form.firstname.data, 'lastname' : form.lastname.data, 'email' : form.email.data, 
                    'street' : form.street.data, 'city' : form.city.data, 'location' : form.location.data}
        data = json.dumps(datax, sort_keys=True, indent=4)
        r = requests.post(url = apiUrl + '/api/v1/patient/', data = data)

        response = json.loads(r.text)

        return redirect(url_for('patienten'))

    return render_template('addpatient.html', form=form)

@app.route('/zoeken', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search', term=form.term.data, type=form.type.data))
    return render_template('search.html', form=form)

@app.route('/search/<type>/<term>') 
def search(type, term):
    if type == "nurse":
        info = urllib.request.urlopen(apiUrl+'/api/v1/nurse/_id='+term)
        info = json.loads(info.read())[0]

    if type == "patient":
        info = urllib.request.urlopen(apiUrl+'/api/v1/patient/_id='+term)
        info = json.loads(info.read())[0]

    print(type)

    return render_template('show.html', info=info, term=term)

#Define main APP
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080", debug=True)