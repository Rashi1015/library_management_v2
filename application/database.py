from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_wtf import CSRFProtect
db = SQLAlchemy()
csrf = CSRFProtect()
security= Security

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)