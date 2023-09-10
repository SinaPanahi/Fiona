from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from datetime import datetime
from fiona import db

class Message(db.Model):
    __tablename__ = 'messages'
    id          = Column(Integer, primary_key=True, autoincrement=True)
    email       = Column(String(200), nullable=False)
    subject     = Column(String(200), nullable=False)
    message     = Column(Text, nullable=False)
    read        = Column(Boolean, nullable=False, default=False)
    since       = Column(DateTime, nullable=False)

    def __init__(self, email, subject, message):
        self.email = email
        self.subject = subject
        self.message = message  
        self.since = datetime.utcnow()  

    def __repr__(self):
        return f'''<User('{self.id}', '{self.email}', '{self.subject}', '{self.message}', '{self.since}')>'''