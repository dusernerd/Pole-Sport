import os
from flask import Flask, request, render_template, redirect, flash, session, url_for
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

app = Flask(__name__)

db = SQL("sqlite:///users.db")


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("email"):
            return apology("Must provide email", 403)
        if not request.form.get("password"):
            return apology("Something went wrong with password", 403)
        row = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))
        if len(row) != 1 or not check_password_hash(row[0]["password"], request.form.get("password")):
           return apology("invalid username and/or password", 403)
        session["user_id"] = row[0]["id"]
        print(session["user_id"])
        return redirect("/")
    else:
        return render_template("login.html")


@app.route("/", methods=["GET","POST"])
@login_required
def index():
    if request.method == "POST":
        sport_id = request.form.get("reg_sport")
        sport_id_desc = request.form.get("des_sport")
        if sport_id:
            rows = db.execute("SELECT * FROM enrollment WHERE user_id=? AND sport_id=?",session["user_id"], sport_id)
            print(len(rows))
            print(rows)
            if len(rows) == 0:
                db.execute(
                        "INSERT INTO enrollment (user_id, sport_id) VALUES (?,?)", session["user_id"], sport_id)
                flash("Successfully registered")

            else:
                return apology("Already Registered OR Invalid Sport")
        print(sport_id_desc)
        rows = db.execute("SELECT sport_id FROM enrollment WHERE user_id=? AND sport_id=?",session["user_id"], sport_id_desc)
        if sport_id_desc:
            print(rows)
            if len(rows) == 1:
                db.execute(
                        "DELETE FROM enrollment WHERE sport_id=?", sport_id_desc)
                session.pop('_flashes', None)
                flash("Successfully UnRegistered")
            else:
                return apology("Already UnRegistered, Or haven't been registered")

        return redirect("/")
    else:
        sports = db.execute("SELECT * FROM sports")
        name = db.execute("SELECT email FROM users WHERE id=?",session["user_id"])
        data = db.execute("SELECT sport FROM users JOIN enrollment ON enrollment.user_id=users.id JOIN sports ON sports.id=enrollment.sport_id WHERE users.id=?", session["user_id"])
        print(data)
        return render_template("index.html", sports=sports, name=name[0]['email'],data=data)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        if not email:
            return apology("must provide username", 400)
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not password or not confirmation:
            return apology("Must provide passwords' fields", 400)
        if password != confirmation:
            return apology("Passwords do not match", 400)
        try:
            # Return id
            new_user = db.execute("INSERT INTO users (email,password) VALUES (?,?);", email, generate_password_hash(password))
            print(new_user)
        except:
            return apology("username is arleady registered")
        session["user_id"] = new_user

        return redirect("/login")
    else:
        return render_template("signup.html")

@app.route("/logout")
def logout():

        session.clear()
        return redirect("/")
