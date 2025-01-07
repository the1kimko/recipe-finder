from sqlalchemy_serializer import SerializerMixin
from models import db

class ShoppingList(db.Model, SerializerMixin):
    __tablename__ = 'shoppinglists'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)

    serialize_rules = ('-user.password', '-user.email')