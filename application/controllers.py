from flask import Flask, render_template, redirect, request
from flask import current_app as app 
from .models import *

sample_data=[{"username":"shivansh", "password":"vani1015","section":'mathematics', "date":"02/02/2004", "description":"master blaster"}]


@app.route("/userlogin", methods=["GET", "POST"])
def user_login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        for data in sample_data:
            if data["username"]== username:
                if data["password"]==password:
                    return render_template("user_dashboard.html", username= username)
                else:
                    return "incorrect Password"
            else:
                return "User does not Exist"

    return render_template('user_login.html')

@app.route("/userregister", methods=["GET", "POST"])
def user_register():
    return render_template('user_register.html')

@app.route("/userdashboard", methods=["GET", "POST"])
def user_dashboard():
    return render_template('user_dashboard.html')



@app.route("/sectionmanagement", methods=["GET", "POST"])
def section_management():
    if request.method == "POST":
    
        section = request.form.get("section")
        date = request.form.get("date")
        description = request.form.get("description")
        image = request.files.get("image")
        if image:
            image.save("uploads/" + image.filename)
        
        return render_template("add_sections.html", section=section, date=date, description=description)

    return render_template("section_management.html")

@app.route("/bookmanagement", methods=["GET", "POST"])
def book_management():
    return render_template('book_management.html')


@app.route("/addsections", methods=["GET", "POST"])
def add_sections():
    
    return render_template('add_sections.html')

@app.route("/librarianlogin", methods=["GET", "POST"])
def librarian_login():
    return render_template('librarian_login.html')

@app.route("/librariandashboard", methods=["GET", "POST"])
def librarian_dashboard():
    return render_template('librarian_dashboard.html')