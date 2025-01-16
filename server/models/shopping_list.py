from sqlalchemy_serializer import SerializerMixin
from models import db

class ShoppingList(db.Model, SerializerMixin):
    __tablename__ = 'shoppinglists'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=True)  # Quantity of the item
    unit = db.Column(db.String(50), nullable=True)  # Unit of measurement

    serialize_rules = ('-user.password', '-user.email', '-recipe.users')