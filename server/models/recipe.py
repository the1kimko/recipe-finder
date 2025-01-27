from sqlalchemy_serializer import SerializerMixin
from models import db

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    spoonacular_id = db.Column(db.Integer, nullable=False, unique=True)  # Spoonacular Recipe ID
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    ingredients = db.Column(db.Text, nullable=False)  # Comma-separated string
    instructions = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=True, default="https://example.com/default-recipe.png")
    source_url = db.Column(db.String(255), nullable=True)  # Original recipe link
    ready_in_minutes = db.Column(db.Integer, nullable=True)  # Preparation time
    servings = db.Column(db.Integer, nullable=True)  # Number of servings
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Null for default recipe

    # Relationships
    favorites = db.relationship('Favorite', back_populates='recipe', lazy=True)  # Many-to-Many via Favorite
    shopping_list = db.relationship('ShoppingList', backref='recipe', lazy=True)  # One-to-Many

    # Serialization Rules
    serialize_rules = ('-favorites.recipe', '-shopping_list.recipe')
