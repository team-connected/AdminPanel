from flask import Flask, render_template, redirect, url_for, session, g, current_app, request
from flask_oidc import OpenIDConnect
from okta import UsersClient
from forms import SearchForm
import requests
import urllib.request
import json
import unicodedata
import os
import pyfiglet

#ENV Flags
apiUrl = os.getenv("api_url", "http://umc-api.maartenmol.nl:5000")

#Print some usefull information to console
ascii_banner = pyfiglet.figlet_format("UMC Data-API")
print(ascii_banner)
print("Starting AdminPanel")
print("API Server Version: V1.0")
print("Developed by: Haydn Felida, Jeroen Verkerk, Sam Zandee, Shaniah Arrias, Maarten Mol. (All rights reserved)")

#Define APP
app = Flask(__name__)

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

@app.route("/showpatient=<id>")
def patient(id):
    data = urllib.request.urlopen(apiUrl+'/api/v1/patient/_id='+id)
    data = json.loads(data.read())[0]

    info = urllib.request.urlopen(apiUrl+'/api/v1/metric/patient='+id)
    info = json.loads(info.read())

    return render_template("patient.html", data=data, metrics=info)

@app.route("/shownurse=<id>")
def nurse(id):
    data = urllib.request.urlopen(apiUrl+'/api/v1/nurse/_id='+id)
    data = json.loads(data.read())[0]

    return render_template("nurse.html", data=data)

@app.route('/removemetric=<id>&patient=<pid>')
def removeMetric(pid,id):
    request = urllib.request.Request(apiUrl+'/api/v1/metric/patient='+pid+'/id='+id, method='DELETE')
    urllib.request.urlopen(request)
    return redirect(redirect_url())

@app.route('/searchUser', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search', email=form.email.data))
    return render_template('search.html', form=form)

@app.route('/search/<email>')
def search(email):
    info = urllib.request.urlopen(apiUrl+'/api/v1/users/email='+email)
    info = json.loads(info.read())[0]

    data = urllib.request.urlopen(apiUrl+'/api/v1/workouts/email='+email)
    data = json.loads(data.read())

    return render_template('show.html', info=info, data=data)

@app.route('/removeWorkout/email=<email>/id=<id>')
def removeWorkout(email,id):
    request = urllib.request.Request(apiUrl+'/api/v1/workouts/user='+email+'/id='+id, method='DELETE')
    urllib.request.urlopen(request)
    return redirect(redirect_url())

#Define main APP
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080", debug=True)