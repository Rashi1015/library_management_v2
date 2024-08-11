from flask import request, jsonify
from flask_restful import Resource, Api, fields, reqparse, marshal_with
from flask_security import auth_required, current_user
from application.models import Book as BookModel, Request, db
from datetime import datetime, timedelta

# Initialize API
api = Api(prefix='/api')

# Request parser for creating books
book_parser = reqparse.RequestParser()
book_parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
book_parser.add_argument('content', type=str, required=True, help="Content cannot be blank!")
book_parser.add_argument('author', type=str, required=True, help="Author cannot be blank!")
book_parser.add_argument('section_id', type=int, required=True, help="Section ID cannot be blank!")

# Request parser for book requests
request_parser = reqparse.RequestParser()
request_parser.add_argument('book_id', type=int, required=True, help="Book ID cannot be blank!")


section_fields = {
    'id': fields.Integer,
    'name': fields.String,
}

books_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'content': fields.String,
    'author': fields.String,
    'date_issued': fields.DateTime,
    'section_id': fields.Integer,
    'section': fields.Nested(section_fields),
}

# Define fields for Request
request_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'book_id': fields.Integer,
    'book': fields.Nested({
        'id': fields.Integer,
        'name': fields.String,
        'author': fields.String,
        'section': fields.Nested(section_fields),
    }),
    'request_date': fields.DateTime,
    'return_date': fields.DateTime,
    'status': fields.String,
}

class Book(Resource):
    @auth_required('token')
    @marshal_with(books_fields)
    def get(self):
        all_books = BookModel.query.all()
        return all_books
    
    @auth_required('token')
    def post(self):
        args = book_parser.parse_args()
        print(args)
        book = BookModel(
            name=args.name,
            content=args.content,
            author=args.author,
            section_id=args.section_id
        )
        db.session.add(book)
        db.session.commit()
        return {'message': 'Book created'}, 200
        
class RequestBook(Resource):
    @auth_required('token')
    @marshal_with(request_fields)
    def get(self):
        user_id = current_user.id
        all_requests = Request.query.filter_by(user_id=user_id).all()
        return all_requests
    
    @auth_required('token')
    def post(self):
        args = request_parser.parse_args()  # Use request_parser instead of book_parser
        book_id = args.book_id  # Extract book_id from the parsed arguments
        
        user_id = current_user.id
        
        # Check if the user has reached the limit of requested or issued books
        requested_books_count = Request.query.filter_by(user_id=user_id, status='requested').count()
        issued_books_count = Request.query.filter_by(user_id=user_id, status='issued').count()
        total_books_count = requested_books_count + issued_books_count

        if total_books_count >= 5:
            return {"message": "You cannot have more than 5 books in requested or issued status."}, 400

        # Create a new book request
        new_request = Request(
            user_id=user_id,
            book_id=book_id,
            request_date=datetime.utcnow(),
            return_date=Request.get_default_return_date()
        )
        db.session.add(new_request)
        db.session.commit()

        return {"message": "Book requested successfully."}, 200

# Add resources to API
api.add_resource(Book, '/books')
api.add_resource(RequestBook, '/request_book')