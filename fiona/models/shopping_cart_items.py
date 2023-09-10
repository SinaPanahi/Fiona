from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from fiona import db

class Shopping_Cart_Item(db.Model):
    __tablename__ = 'shopping_cart_items'

    id          = Column(Integer, primary_key=True, autoincrement=True)
    user_id     = Column(Integer, ForeignKey('users.id'), nullable=False)
    painting_id = Column(Integer, ForeignKey('paintings.id'), nullable=False)
    since       = Column(DateTime, nullable=False, default=datetime.utcnow)

    user = relationship("User")
    painting = relationship("Painting")
       

    def __init__(self, user_id, painting_id):
        self.user_id = user_id
        self.painting_id = painting_id

    def __repr__(self):
        return f'''<Shopping_Cart_Item('{self.id}', '{self.user_id}', '{self.painting_id}', '{self.since}'>'''