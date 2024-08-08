from flask import render_template,Flask, redirect, flash, url_for, make_response, request, session, render_template_string
from flask import current_app as app 
from application.models import *
import pdfkit
from sqlalchemy import func, or_
from flask_security import hash_password,login_user, auth_required, roles_accepted, current_user, roles_required
import uuid
from flask_security import SQLAlchemySessionUserDatastore
from .sec import user_datastore
from flask import jsonify
from flask_security.utils import verify_password


config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')



def create_views(app,user_datastore: SQLAlchemySessionUserDatastore ):
    @app.route('/userlogin', methods=['POST'])
    def user_login():
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        current_user = User.query.filter_by(username=username).first()

        if current_user:
            if verify_password(password, current_user.password):
                session['user_id'] = current_user.id
                session['username'] = current_user.username
                session['logged_in'] = True
                token = current_user.get_auth_token()  
                session['role'] = current_user.role
                
                response = {
                    "message": "Login successful",
                    "token": token,
                    "role" : current_user.roles[0].name,
                    "redirect": "/userdashboard" if current_user.roles[0].name != "admin" else "/librariandashboard"
                }
                return jsonify(response), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    
    @app.route('/userregister', methods=['POST'])
    def user_register():
        data = request.get_json()
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

    @app.route('/logout')
    def logout():
        session.clear()
        return jsonify({"message": "Logged out successfully"}), 200

    @app.route('/userdashboard', methods=["GET", "POST"])
    @auth_required('token')
    def user_dashboard():
        user_id = session.get('user_id')
        username = session.get('username')

        if not user_id or not username:
            return jsonify({"redirect": "/userlogin", "message": "Please log in to access your dashboard."}), 403

        search_word = request.args.get('search_word', '')
        if search_word:
            search_word = "%" + search_word + "%"
            books_by_name = Book.query.filter(Book.name.ilike(search_word)).all()
            books_by_author = Book.query.filter(Book.author.ilike(search_word)).all()
            books_by_section = Book.query.join(Section).filter(Section.name.ilike(f'%{search_word}%')).all()
            books = books_by_name + books_by_author + books_by_section
        else:
            books = Book.query.all()

        book_details = []
        for book in books:
            section = book.section
            book_details.append({
                "id": book.id,
                'name': book.name,
                'author': book.author,
                'section': section.name
            })

        if request.method == "POST":
            data = request.get_json()
            book_id = data.get('book_id')
            
            if not book_id:
                return jsonify({"message": "Book ID is required."}), 400
            
            requested_books_count = Request.query.filter_by(user_id=user_id, status='requested').count()
            issued_books_count = Request.query.filter_by(user_id=user_id, status='issued').count()
            total_books_count = requested_books_count + issued_books_count

            if total_books_count >= 5:
                return jsonify({"message": "You cannot have more than 5 books in requested or issued status."}), 400

            new_request = Request(
                user_id=user_id,
                book_id=book_id,
                request_date=datetime.utcnow(),
                return_date=Request.get_default_return_date()
            )
            db.session.add(new_request)
            db.session.commit()
            return jsonify({"message": "Book request submitted successfully.", "redirect": "/userbooks"}), 201

        return jsonify({"username": username, "book_details": book_details, "user_id": user_id}), 200

        
    @app.route('/assign_admin', methods=['POST'])
    @auth_required('token')
    def assign_admin():
        data = request.get_json()
        user_id = data.get("user_id")
        user = User.query.get(user_id)
        
        new_role_name = "admin"
        new_role = Role.query.filter_by(name=new_role_name).first()

        user.roles = []
        db.session.commit()
        user.roles.append(new_role)
        user.role = new_role.name  # Update the role column in the User table
        db.session.commit()

        return jsonify({"message": f"Role updated to {new_role_name}"}), 200



# Run your application
if __name__ == '__main__':
    app.run(debug=True)