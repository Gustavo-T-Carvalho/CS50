import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        day = request.form.get("day")
        month = request.form.get("month")

        if (not month or not day or not name):
            return redirect("/")

        db.execute(
            "INSERT INTO birthdays (name, month, day) VALUES (?,?,?);", name, int(month), int(day))
        return redirect("/")

    else:
        birthdays = db.execute("SELECT * FROM birthdays;")
        return render_template("index.html", birthdays=birthdays)


@app.route("/exclude", methods=["POST"])
def exclude():
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM birthdays WHERE id = ?", id)
    return redirect("/")


@app.route("/update", methods=["GET", "POST"])
def update():

    if request.method == "POST":
        id = request.form.get("id")
        name = request.form.get("name")
        day = request.form.get("day")
        month = request.form.get("month")
        print(id)
        if (not month or not day or not name or not id):
            return redirect("/")

        db.execute(
            "UPDATE birthdays SET name=?, month=?, day=? WHERE id=?;", name, int(month), int(day), int(id))
        return redirect("/")
    else:
        id = request.args.get("id")
        if (not id):
            return redirect("/")

        entry = db.execute("SELECT * FROM birthdays WHERE id = ?;", id)
        if (not len(entry)):
            return redirect("/")

        return render_template("update.html", birthday=entry[0])
