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




def create_view():
    @app.route('/')
    def home():
        return render_template('index.html') # entry point to vue frontend