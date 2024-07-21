from flask_sqlalchemy import SQLAlchemy
from flask_security import Security

db = SQLAlchemy()
security= Security

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)