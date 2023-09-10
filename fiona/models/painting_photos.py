from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from datetime import datetime
from fiona import db

class Painting_Photo(db.Model):
    __tablename__ = 'painting_photos'

    id          = Column(Integer, primary_key=True, autoincrement=True)
    painting_id = Column(Integer, ForeignKey('paintings.id'), nullable=False)
    url         = Column(String(256), nullable=False, unique=True)
    since       = Column(DateTime, nullable=False, default=datetime.utcnow)

    painting = relationship("Painting")

    def __init__(self, painting_id, url):
        self.painting_id = painting_id
        self.url = url

    def __repr__(self):
        return f'''<Painting_Photo('{self.id}', '{self.painting_id}', '{self.url}', '{self.since}'>'''