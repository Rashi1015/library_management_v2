from flask import render_template, redirect, flash, url_for, make_response, request, session, render_template_string
from flask import current_app as app 
from application.models import *
import pdfkit
from sqlalchemy import func, or_
from flask_security import hash_password, auth_required, roles_accepted, current_user
import uuid
from .sec import user_datastore
from flask import jsonify
from flask_security.utils import verify_password


config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')




def create_views(app):
    @app.route('/userlogin', methods=['POST'])
    def user_login():
        data = request.json

        username = data.get("username")
        password = data.get("password")
        current_user = User.query.filter_by(username=username).first()

        if current_user:
            if verify_password(password, current_user.password):
                session['user_id'] = current_user.id
                session['username'] = current_user.username
                session['logged_in'] = True
                if current_user.roles[0].name == "admin":
                    return jsonify({"redirect": "/librariandashboard"})
                else:
                    return jsonify({"redirect": "/userdashboard"})
            else:
                return jsonify({"error": "Incorrect Password"}), 400
        else:
            return jsonify({"error": "User does not Exist"}), 400

    @app.route('/userregister', methods=['POST'])
    def user_register():
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({"error": "Username or password not provided"}), 400

        # Generate a unique fs_uniquifier
        fs_uniquifier = str(uuid.uuid4())
        # Create the user
        try:
            user_datastore.create_user(
                username=username,
                password=hash_password(password),
                active=True,
                fs_uniquifier=fs_uniquifier,
                roles=['user']
            )
            db.session.commit()
            return jsonify({"message": "User registered successfully", "redirect": "/userlogin"}), 201
        except Exception as e:
            print("Error:", e)  # Debugging statement to print the error
            return jsonify({"error": "User registration failed"}), 500

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/userdashboard')
    def user_dashboard():
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

# Run your application
if __name__ == '__main__':
    app.run(debug=True)