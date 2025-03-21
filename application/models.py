from .database import *
from datetime import datetime, timedelta
from flask_security import UserMixin, RoleMixin
from flask_security.models import fsqla_v3 as fsq
#from flask_wtf.csrf import CSRFProtect, generate_csrf
fsq.FsModels.set_db_info(db)

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    extend_existing=True
)

    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    role = db.Column(db.String(20), nullable=False, default="user")  # 'admin' or 'user'

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    librarian_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    librarian = db.relationship('User', backref=db.backref('sections', lazy=True))

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date_issued = db.Column(db.DateTime, default=datetime.utcnow)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'), nullable=False)
    section = db.relationship('Section', backref=db.backref('books', lazy=True))




class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = db.relationship('Book', backref=db.backref('requests', lazy=True))
    request_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=False)
    user = db.relationship('User', backref=db.backref('requests', lazy=True))
    status = db.Column(db.String(20), nullable=False, default='requested')  # 'issued', 'paid', 'rejected'

    @staticmethod
    def get_default_return_date():
        # Set the default return date to 7 days from the request date
        return datetime.utcnow() + timedelta(days=7)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = db.relationship('Book', backref=db.backref('feedbacks', lazy=True))
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('ratings', lazy=True))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = db.relationship('Book', backref=db.backref('ratings', lazy=True))
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Rating(id={self.id}, user_id={self.user_id}, book_id={self.book_id}, rating={self.rating})"
