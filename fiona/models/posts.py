from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from fiona import db

class Post(db.Model):
    __tablename__ = 'posts'
    id          = Column(Integer, primary_key=True, autoincrement=True)
    title       = Column(String(256), nullable=False)
    text        = Column(Text, nullable=False)
    url         = Column(String(256), nullable=True, unique=True)
    since       = Column(DateTime, nullable=False)
      
    def __init__(self, title, text, url=None):
        self.title = title
        self.text = text
        self.url = url
        self.since = datetime.utcnow()

    def __repr__(self):
        return f'''<Post('{self.id}', '{self.title}', '{self.text}', '{self.url}', '{self.since}')>'''