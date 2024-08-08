from flask import request, jsonify
from flask_restful import Resource, Api, fields, reqparse, marshal_with
from flask_security import auth_required, current_user
from application.models import Book as BookModel, Section, db

api = Api(prefix='/api')
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help="Name cannot be blank!")
parser.add_argument('content', type=str, required=True, help="Content cannot be blank!")
parser.add_argument('author', type=str, required=True, help="Author cannot be blank!")
parser.add_argument('section_id', type=int, required=True, help="Section ID cannot be blank!")

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

class Book(Resource):
    @auth_required('token')
    @marshal_with(books_fields)
    def get(self):
        all_books = BookModel.query.all()
        return all_books
    
    @auth_required('token')
    def post(self):
        args = parser.parse_args()
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
        
api.add_resource(Book, '/books')
