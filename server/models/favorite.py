from sqlalchemy_serializer import SerializerMixin
from models import db

class Favorite(db.Model, SerializerMixin):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    recipe_title = db.Column(db.String(200), nullable=False)

    # Relationships
    user = db.relationship('User', back_populates='favorites')
    recipe = db.relationship('Recipe', back_populates='users')

    serialize_rules = ('-user.password', '-user.email', '-recipe.shopping_list') 