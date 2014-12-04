# -*- coding: utf-8 -*-
"""
Created on Sat Oct 04 14:54:34 2014

@author: Carko
"""

from flask import *
from functools import wraps
import sqlite3

DATABASE = "sales.db"

app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = "my precious"

def connect_db():
    return sqlite3.connect(app.config["DATABASE"])

@app.route('/')
def home():
    return render_template("home.html")
    
@app.route('/for')
def fore():
    text="<html><body>"
    for i in range(1,101):
        text=text+str(i)+". obrazek<br>"
    text=text+"</body></html>"
    return text
    
@app.route('/welcome')
def welcome():
    return render_template("welcome.html")
    
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("You need to be logged in first.")
            return redirect(url_for("log"))
    return wrap
    
@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("You have logged out")
    return redirect (url_for("log"))
    
@app.route('/logok')
@login_required
def logok():
    g.db = connect_db()
    cur = g.db.execute("select rep_name, amount from reps")
    sales = [dict(rep_name=row[0], amount=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template("logok.html", sales=sales)
    
@app.route('/log', methods=["GET", "POST"])
def log():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again'
        else:
            session["logged_in"] = True
            return redirect(url_for("logok"))
    return render_template("log.html", error=error)


if __name__ == '__main__':
    app.run(debug=True)