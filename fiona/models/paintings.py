from sqlalchemy import Column, Integer, String, Text, Boolean
from datetime import datetime
from fiona import db

class Painting(db.Model):
    __tablename__ = 'paintings'
    id                  = Column(Integer, primary_key=True, autoincrement=True)
    name                = Column(String(128), unique=True, nullable=False)
    description         = Column(Text, nullable=False)
    width               = Column(Integer, nullable=False)
    height              = Column(Integer, nullable=False)
    price               = Column(String(64), nullable=False)
    url                 = Column(String(256), nullable=False, unique=True)
    is_carousel_item    = Column(Boolean, nullable=False, default=False)
    is_sold             = Column(Boolean, nullable=False, default=False)
       

    def __init__(self, name, description, width, height, price, url, is_carousel_item):
        self.name = name
        self.description = description
        self.width = width
        self.height = height
        self.price = price
        self.url = url
        self.is_carousel_item = is_carousel_item

    def __repr__(self):
        return f'''<Painting('{self.id}', '{self.name}', '{self.description}', '{self.width}',
                         '{self.height}', '{self.price}, '{self.url}' , '{self.is_carousel_item}, '{self.is_sold}'>'''