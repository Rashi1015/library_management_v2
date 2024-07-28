from flask import render_template, redirect, flash, url_for, make_response, request, session, render_template_string
from flask import current_app as app 
from application.models import *
import pdfkit
from sqlalchemy import func, or_
from flask_security import hash_password, auth_required, roles_accepted, current_user
import uuid
from .sec import user_datastore
from flask import jsonify



config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')




def create_views(app):
    @app.route('/userlogin', methods=['POST'])
    def user_login():
        data = request.json
        username = data.get("username")
        password = data.get("password")
        current_user = User.query.filter_by(username=username).first()

        if current_user:
            if current_user.password == password:
                session['user_id'] = current_user.id
                session['username'] = current_user.username
                session['logged_in'] = True
                if current_user.role == "admin":
                    return jsonify({"redirect": "/librariandashboard"})
                else:
                    return jsonify({"redirect": "/userdashboard"})
            else:
                return jsonify({"error": "Incorrect Password"}), 400
        else:
            return jsonify({"error": "User does not Exist"}), 400

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/profile')
    @auth_required('token', 'session')
    def profile():
        return render_template_string(
            """
                <h1> this is homepage </h1>
                <p> Welcome, {{current_user.email}}</p>
                <p> Role :  {{current_user.roles[0].description}}</p>
                <p><a href="/logout">Logout</a></p>
            """
        )
create_views(app)