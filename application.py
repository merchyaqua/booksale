import os
import re


from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, ordinal

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# DB variable
# Create engine object to manage connections to DB, and scoped session to separate user interactions with DB
engine = create_engine(os.getenv("postgres://sumjznccdlzznq:3f1d52a46872bf40a37c9f7a775a6596e4a04c1e3da8be50ab9ef09647cf0ede@ec2-35-175-155-248.compute-1.amazonaws.com:5432/dc6vvaofgcagpo"))
db = scoped_session(sessionmaker(bind=engine))


# connection = psycopg2.connect(database="d290ae7p5vcp2v", user="awywxapixuwmgj", password="69d423becb0ed39ecf4493a9beaf3589c02784505c7937dd61129f206139be46", host="ec2-54-236-169-55.compute-1.amazonaws.com", port=5432)

# db = connection.cursor()
#session["friends_id"] = ""

@app.route("/", methods=["GET", "POST"])
@login_required
def db():
    """Show welcome and recent entries, status etc."""
    if request.method == "POST":
        db.execute("INSERT INTO test VALUES :a", {"a": request.form.get("a")})
    table = db.execute("SELECT field FROM test").fetchone[0]
    return render_template("index.html", table=table)