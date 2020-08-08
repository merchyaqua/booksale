import os
import re
import smtplib, ssl

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, login_required, ordinal, convertSQLToDict

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
engine = create_engine("postgres://sumjznccdlzznq:3f1d52a46872bf40a37c9f7a775a6596e4a04c1e3da8be50ab9ef09647cf0ede@ec2-35-175-155-248.compute-1.amazonaws.com:5432/dc6vvaofgcagpo")
db = scoped_session(sessionmaker(bind=engine))


# connection = psycopg2.connect(database="d290ae7p5vcp2v", user="awywxapixuwmgj", password="69d423becb0ed39ecf4493a9beaf3589c02784505c7937dd61129f206139be46", host="ec2-54-236-169-55.compute-1.amazonaws.com", port=5432)

# db = connection.cursor()
#session["friends_id"] = ""

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show welcome and recent entries, status etc."""
    if request.method == "POST":
        db.execute("INSERT INTO test (field) VALUES (:a);", {"a": request.form.get("a")})
        db.commit()
        return redirect("/")
    return render_template("index.html")




@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "POST":
        un = request.form.get("changeun")
        pw = request.form.get("changepw")
        pw2 = request.form.get("changepw2")

        # setting status of user, by default its publicstatus = request.form.get("status")if status == "PRIV":db.execute("UPDATE users SET status = :s WHERE id = :u", {"s": status, "u": session["user_id"]})

        #if request.form.get("status"):db.execute("UPDATE users SET status = 'PRIV' WHERE id = :u", u=session["user_id"])
        if pw:
            rows = db.execute("SELECT * FROM users WHERE username = :username", {'username':session["username"]}).fetchall()
            # Ensure username exists and password is correct
            if not check_password_hash(rows[0]["hash"], request.form.get("old")):
                flash("Old password incorrect :/")
                return apology("Your password is not correct. Try again!", 403)
                return redirect("/account")
            db.execute("UPDATE users SET hash = :p, length = :l WHERE id = :i", {'u':un, 'p': generate_password_hash(pw) ,'l':len(pw), 'i':session['user_id']})
            db.commit()
            return redirect('/account')


        user = db.execute("SELECT * FROM users WHERE username = :username AND id != :i", {'username':session["username"], 'i':session["user_id"]}).fetchall()
        if user:
            return apology("Username is already taken,", 403)
        elif re.search(" ", un):
            return apology("Username must not contain spaces,")
        # Ensure password was up to specs
        elif len(un) > 15 :
            return apology("Username is limited to 15 characters,")
        #else:db.execute("UPDATE users SET status = 'PUB' WHERE id = :u", {'u':session["user_id"]})
        db.execute("UPDATE users SET username = :u, first = :f, last = :l, class = :c, number = :n WHERE id = :i",
                   {'u':un, 'f': request.form.get("first"), 'l': request.form.get("last"), 'c': request.form.get("class"), 'n':request.form.get("number"), 'i':session['user_id']})
        db.commit()
        session["username"] = un
        session["first"] = request.form.get("first")
        session["last"] = request.form.get("last")
        if session["number"]:
            session["class"] = request.form.get("class")
            session["number"] = request.form.get("number")
        return redirect ("/account")
    length = db.execute("SELECT length FROM users WHERE id = :u", {'u':session["user_id"]}).fetchone()[0]
    return render_template("account.html", u=session["user_id"], stars="*" * length)#, status=status[0]["status"]

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    """New Entries"""
    if request.method == "POST":
        forms = request.form.getlist("form")
        subjects = request.form.getlist("subject")
        f = ''
        s = ''
        for form in forms:
            f = f + ' ' + form
        for subject in subjects:
            s = s + ' ' + subject
        # if no title, replace with /
        u = session["user_id"]
        # insert
        db.execute("INSERT INTO posts (id, form, subject, description, link, contact, title) VALUES (:i, :f, :s, :d, :l, :c, :t)", 
        {'i': session["user_id"], 'f':f, 's':s, 'd':request.form.get("description"), 'l':request.form.get("link"), 'c':request.form.get("contact"), 't':request.form.get("title")})
        print("Entry inserted.")
        return redirect("/entries")
    return render_template("post.html")


@app.route("/posts/sellers")
@login_required
def sellers():
    table = convertSQLToDict(db.execute("SELECT * FROM posts WHERE buyorsell = 'sell' ORDER BY postid DESC LIMIT 50").fetchall())
    for row in table:
        seller = db.execute("SELECT username, first, last, class, number FROM users WHERE id = :i", {"i": row["id"]}).fetchone()
        if seller['number']:
            full = f"{row['id']} {seller['username']} {seller['class']} {seller['number']} {seller['first']} {seller['last']}"
        else:
            full = f"{row['id']} {seller['username']} {seller['first']} {seller['last']}"

        row.update({"seller": full})
    return render_template("sellers.html", table=table)


@app.route("/posts/buyers")
@login_required
def buyers():
    return

@app.route('/posts/<postid>')
@login_required
def viewpost(postid):

    return

@app.route('/sort', methods=["POST"])
@login_required
def sort():
    page = request.form.get("page")
    return redirect("")
















@app.route("/booklists")
@login_required
def booklists():
    return render_template("booklists.html")


@app.route("/help")
def helpo():
    return render_template("help.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # done by javascript disable
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          {'username':request.form.get("username")}).fetchall()
        print(rows)
        # Ensure username exists and password is correct
        if len(rows) != 1 :
            return apology("Your username is not found,", 403)
        elif not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Your password is not correct. Try again!", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        session["class"] = rows[0]["class"]
        session["number"] = rows[0]["number"]
        session["first"] = rows[0]["first"]
        session["last"] = rows[0]["last"]

        print("Logged in " + session["username"] + ", ID " + str(session["user_id"]) + " at " + datetime.now().strftime("%m/%d/%Y %H:%M:%S"))
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        i = request.form.get("id")
        e = request.form.get("email")
        if i or e:
            if i:
                d = i
            else:
                d = e
            try:
                # if registered
                user = db.execute("SELECT username FROM users WHERE id = :i", {"i": d}).fetchone()[0].lower()
                print("returning apology for existence")
                return apology(f"Wait...this user is registered on the site as {user}.\n Not you? I'll fix it and investigate🕵️‍♀️(if you wish),", 403)
            except:
                # if not on list (NOL) well, not found
                try:
                    user = db.execute("SELECT * FROM users WHERE id = :i", {"i": d}).fetchall()[0]
                except:
                    print("returning apology for not on list")
                    return apology("NOL", 404)
                print("returning form")
                school = re.search(user['id'], '@')
                return render_template("register.html", user=user, school=school)


        pw = request.form.get("password")
        c = request.form.get("confirmation")
        un = request.form.get("username")
        # Ensure username was unique

        user = db.execute("SELECT * FROM users WHERE username = :username", {'username':un}).fetchone()[0]
        if user:
            return apology("Username is already taken,", 403)
        elif re.search(" ", un):
            return apology("Username must not contain spaces,")
        # Ensure password was up to specs
        elif len(un) > 15 :
            return apology("Username is limited to 15 characters,")
        elif c != pw:
            return apology("Passwords don't match,")
        elif len(pw) < 8:
            return apology("Your password is too short,")
        # database insert
        db.execute("UPDATE users SET username = :u, hash = :p, length = :l WHERE id = :i",
                   {'u':un, 'p': generate_password_hash(pw) , 'l':len(pw), 'i':user['id']})
        # Remember which user has logged in
        session["user_id"] = db.execute("SELECT id FROM users WHERE username = :username",
                                        {'username':un}).fetchone()[0]


        # setting status of user, by default its public
        status = request.form.get("status")
        if status == "PRIV":
             db.execute("UPDATE users SET status = :s WHERE id = :u", {"s": status, "u": session["user_id"]})
        db.commit()

        user = db.execute("SELECT * FROM users WHERE username = :username", {'username':un}).fetchall()[0]
        session["username"] = un
        session["user_id"] = user["user_id"]
        session["class"] = user["class"]
        session["number"] = user["number"]
        session["first"] = user["first"]
        session["last"] = user["last"]
        # Redirect user to home page
        return redirect("/")
    return render_template("register.html")





@app.route("/logout")
@login_required
def logout():
    """Log user out"""
    print("Logging out " + session["username"] + ", ID " + str(session["user_id"]))
    # Forget any user_id
    session.clear()
    print("Done.")
    # Redirect user to login form
    return redirect("/")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
