import os
from flask import Flask, render_template, request, flash, redirect, session
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import enum
from models import Base, User, Task, Category
from werkzeug.security import generate_password_hash
from helpers import login_required


app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
# access to database
engine = create_engine('sqlite:///database.db')
# creating tables in the database in accordance with the models defined in SQLAlchemy. This command transforms the declarative class definitions in my code into corresponding SQL commands that create table structures in the database.
Base.metadata.create_all(engine)

# creating a 'session' allows me to manage databes operations
Session = sessionmaker(bind=engine)
session = Session()


@app.route("/")
@login_required
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
    else:
        if not request.form.get("first_name") or not request.form.get("last_name") or not request.form.get("email") or not request.form.get("password") or not request.form.get("confirm_password") :
            flash("Complete the required fields.", "form_error")
        
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if password != confirm_password:
            flash("Passwords are not identical", "confirm_password_error")
        
        hashed_password = generate_password_hash(password)

        # query database for email
        user = session.query(User).filter_by(email=email).first()
        # if user exists
        if user is not None:
            flash("This email exists in the database. Please log in", "user_exists")
        
        #if user not exists yet
        new_user = User(email=email, password=hashed_password, first_name=first_name, last_name=last_name)
        session.add(new_user)
        session.commit()

        session["user_id"] = new_user.id

        return redirect("/")

@app.route("/addtask", methods=["GET", "POST"])
@login_required
def addtask():
    if request.method == "GET":
        return render_template("addtask.html")
        