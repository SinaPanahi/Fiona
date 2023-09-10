from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from fiona import db

class User(db.Model):
    __tablename__ = 'users'
    # Mandatory upon sign up
    id              = Column(Integer, primary_key=True, autoincrement=True)
    email           = Column(String(200), unique=True, nullable=False)
    password        = Column(String(256), nullable=False)
    is_activated    = Column(Boolean, nullable=False, default=False)
    activation_token= Column(String(256), nullable=False)
    since           = Column(DateTime, nullable=False, default=datetime.utcnow)
    # Mandatory upon purchase
    name            = Column(String(200), nullable=True)
    phone           = Column(String(12), nullable=True)
    province        = Column(String(64), nullable=True)
    city            = Column(String(64), nullable=True)
    street          = Column(String(64), nullable=True)  
    number          = Column(String(12), nullable=True)
    postal_code     = Column(String(7), nullable=True)
    # Only for the website admin
    is_admin    = Column(Boolean, nullable=False, default=False) 

    def __init__(self, email, password, activation_token, is_admin=False):
        self.email = email
        self.is_admin = is_admin
        self.password = password
        self.activation_token = activation_token
    

    def __repr__(self):
        return f'''<User('{self.id}', '{self.email}', '{self.is_activated}', '{self.activation_token}', '{self.name}', '{self.phone}',
                         '{self.province}', '{self.city}', '{self.street}', '{self.number}',
                         '{self.postal_code}', '{self.since}', , '{self.is_admin}')>'''