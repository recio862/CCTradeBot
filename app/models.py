from app.db import db
from sqlalchemy import Column


class Account(db.Model):
    __tablename__ = 'account'

    id = Column(db.Integer, primary_key=True)

class Orders(db.Model):
    __tablename__ = 'order'

    id = Column(db.Integer, primary_key=True)
    order_filled = Column(db.Boolean, default=False)
