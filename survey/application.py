import cs50
import csv

from flask import Flask, jsonify, redirect, render_template, request, url_for
from collections import defaultdict

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def post_form():
    name = request.form.get('name')
    option = request.form.get('home')
    terms = request.form.get('terms')
    radio = request.form.get('gridRadios')

    if (name is None \
        or option is None \
        or terms is None \
        or radio is None):
            return render_template("error.html", message="Fill in all the form fields.")
    else:
        with open('survey.csv', 'w', newline='') as csvfile:
            fieldnames = ['Name', 'House', 'Position']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if csvfile.tell() == 0:
                writer.writeheader()  # file doesn't exist yet, write a header

            writer.writerow({'Name': name, 'House': option, 'Position': radio})
    return redirect(url_for('get_sheet'))


@app.route("/sheet", methods=["GET"])
def get_sheet():
    names = []
    homes = []
    positions = []
    total = 0
    with open('survey.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader, None)  # skip the headers
        for row in reader:
            names.append(row[0])
            homes.append(row[1])
            positions.append(row[2])
    total = len(names)
    return render_template("survey_data.html",
        names = names,
        homes = homes,
        positions = positions,
        total = total)
