import os
from flask import Flask, render_template, request, flash, redirect, session
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import enum
from models import Base, User, Task, PriorityLevel, Categories
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required
from collections import defaultdict
   
app = Flask(__name__)
# secret_key should be hidden 
app.secret_key = 'b(3\xe1\xc2\x0b\xd0J\xc3\xfc\xf9=\xf0\xf2T\x08!\xc5~j6\x9a$\xbf>'
# access to database
engine = create_engine('sqlite:///database.db')
# creating tables in the database in accordance with the models defined in SQLAlchemy. This command transforms the declarative class definitions in my code into corresponding SQL commands that create table structures in the database.
Base.metadata.create_all(engine)

# creating a 'session' allows me to manage databes operations
Session = sessionmaker(bind=engine)
db_session = Session()
 
      
@app.route("/")
@login_required
def index():
    if "user_id" in session:

        user_id = session["user_id"]
        user_data = db_session.query(User).filter_by(id=user_id).all()
        tasks = db_session.query(Task).filter_by(user_id=user_id).order_by( Task.category, Task.completed).all()

        tasks_by_category = defaultdict(list)
        for task in tasks:
            tasks_by_category[task.category.value].append(task)

        return render_template("index.html", user_data=user_data, tasks_by_category=tasks_by_category)
    else:
        return redirect("login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # forget any user_id 
        session.clear()

        if not request.form.get("email") or not request.form.get("password"):
            flash("Complete the required fields.", "form_error")
            return render_template("login.html")
        
        email = request.form.get("email")

        # query database for email
        user = db_session.query(User).filter_by(email=email).first()

        # check if user exists
        #? if user exists and password is correct
        if user is None:
            flash("User does not exist. Please sign in.", "user_error")
            return render_template("login.html")
        else:
            password = user.password
            if not check_password_hash(password, request.form.get("password")):
                flash("Email or password is not correct. Please try again", "login_error")
                return render_template("login.html")
            else:
                session["user_id"] = user.id
                return redirect("/")
   
@app.route("/logout")
def logout():
    # forget any user_id
    session.clear()
    return redirect("/")
          
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        if not request.form.get("first_name") or not request.form.get("last_name") or not request.form.get("email") or not request.form.get("password") or not request.form.get("confirm_password") :
            flash("Complete the required fields.", "form_error")
            return render_template("register.html")
        
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if password != confirm_password:
            flash("Passwords are not the same", "confirm_password_error")
            return render_template("register.html")

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
  
        # query database for email
        user = db_session.query(User).filter_by(email=email).first()
        # if user exists
        if user is not None:
            flash("This user already exists. Please log in", "user_exists")
            return render_template("register.html")

          
        #if user not exists yet
        new_user = User(email=email, password=hashed_password, first_name=first_name, last_name=last_name)
        db_session.add(new_user)
        db_session.commit()

        session["user_id"] = new_user.id
 
        return redirect("/")
 
@app.route("/addtask", methods=["GET", "POST"])
@login_required
def addtask():
    if request.method == "GET":
        # to pass a list of categories to the template, I can do so by converting the Categories enumeration type to a list or dictionary.
        categories = [(cat.name, cat.value) for cat in Categories]
        priority = [(prio.name, prio.value) for prio in PriorityLevel]
        return render_template("addtask.html", categories=categories, priority=priority)
    else: 
        # getting data from the form
        title = request.form.get("title")
        description = request.form.get("description")
        priority = request.form.get('priority')
        category = request.form.get('category')

        if not title or not category or not priority:
            flash("Complete the required fields.", "form_error")
            return render_template("addtask.html", categories=categories, priority=priority)
 
        new_task = Task(
            title = title,
            description = description if description else "No description",
            priority = PriorityLevel[priority],
            category = Categories[category],
            user_id = session["user_id"]
        )

        db_session.add(new_task)
        db_session.commit()

        flash(f"Your task was added successfully", "task_success")
        return redirect("/")


@app.route("/toogle_task/<int:task_id>", methods=["POST"])
@login_required
def toggle_task(task_id):

    task = db_session.query(Task).get(task_id)

    if task:
        task.completed = not task.completed
        db_session.commit()
    else:
        flash("Task not found.", "done_error")
    
    return redirect("/")
    
@app.route("/delete/<int:task_id>", methods=["POST"])
@login_required
def delete(task_id):

    task = db_session.query(Task).get(task_id)

    if task:
        db_session.delete(task)
        db_session.commit()
    else:
        flash("Task not found", "done_error")
    return redirect("/")
             