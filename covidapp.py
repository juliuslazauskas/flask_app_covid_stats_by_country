'''flask web app to get covid-19 data in json format 
from opendata.ecdc.europa.eu and display in one endpoint'''

#importing modules
from flask import Flask, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
import requests

#initialize Flask application
app = Flask(__name__)

# use filesystem for session instead of cookies
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


#setting the default route
@app.route("/", methods = ["GET","POST"])
def main_page():
    if request.method == "GET":
        # load data only once into session variable if reached via GET request
        if not session:
            d_request = requests.get("https://opendata.ecdc.europa.eu/covid19/nationalcasedeath/json/")
            session['data'] = d_request.json()
            session['country_list'] = []
            for item in session['data']:
                if item['country'] not in session['country_list']:
                    session['country_list'].append(item['country'])
        return render_template('mainpage.html', country_list=list(enumerate(session['country_list'])))

    else:
        #when form is submitted (country is selected), we get a POST request and gather neccesary data from session variable
        country_no = int(request.form.get("country_selected"))
        timeline_deaths = []
        deaths = []
        timeline_cases = []
        cases = []
        #selected country data is fetched 
        for item in session['data']:
            if item['country'] == session['country_list'][country_no]:
                if item['indicator'] == 'deaths':
                    timeline_deaths.append(item['year_week'])
                    deaths.append(item['weekly_count'])
                if item['indicator'] == 'cases':
                    timeline_cases.append(item['year_week'])
                    cases.append(item['weekly_count'])
        country = session['country_list'][country_no]
        #and passed to html and JavaScript objects
        return render_template('mainpage.html', country_list=list(enumerate(session['country_list'])),
                                timeline_cases=timeline_cases, cases=cases, timeline_deaths=timeline_deaths,
                                deaths=deaths, country=country) 
