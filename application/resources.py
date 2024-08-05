from flask_restful import Resource, Api, fields, reqparse, marshal_with
from flask_security import auth_required
from application.models import *
api= Api(prefix='/api')
parser = reqparse.RequestParser()

books_fields= {
    'id' : fields.Integer,
    'name' : fields.String,
    'content':fields.String,
    'author':fields.String,
    'date_issued':fields.DateTime,
    'section_id':fields.Integer,
    'section':fields.String,
}

class Book(Resource):
    @auth_required()
    @marshal_with(books_fields)

    def get(self):
        all_books=Book.query.all()
        return all_books
    
    def post(self):
        args = parser.parse_args()
        book = Book(**args) 
        db.session.add(book)
        db.session.commit()
        return {'message': 'book created'}, 200
    
api.add_resource(Book, '/books')