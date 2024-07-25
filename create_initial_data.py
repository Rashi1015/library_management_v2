from flask_security import SQLAlchemyUserDatastore
from flask_security.utils import hash_password
from application.database import *
from werkzeug.security import generate_password_hash
import uuid
from application.models import *

def create_data(user_datastore: SQLAlchemyUserDatastore):

    print('### creating Data ###')

    
    user_datastore.find_or_create_role(name = "user", description ="Regular user")
    user_datastore.find_or_create_role(name = "admin", description ="Administrator")


    if not user_datastore.find_role('admin'):
        user_datastore.create_role(name='admin', description='Administrator')
    if not user_datastore.find_role('user'):
        user_datastore.create_role(name='user', description='Regular user')
    
    if not user_datastore.find_user(username='admin'):
        user_datastore.create_user(username='admin', password=hash_password('password'),active=True,fs_uniquifier=str(uuid.uuid4()), roles=['admin'])
    if not user_datastore.find_user(username='testuser'):
        user_datastore.create_user(username='testuser', password=hash_password('password'),active=True, fs_uniquifier=str(uuid.uuid4()),roles=['user'])

    db.session.commit()

    