from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base



app = Flask(__name__)
# access to database
engine = create_engine('sqlite:///database.db')



@app.route("/")
def index(): 
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

@app.route("/addtask", methods=["GET", "POST"])
def addtask():
    if request.method == "GET":
        return render_template("addtask.html")
        