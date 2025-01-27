from sqlalchemy_serializer import SerializerMixin
from datetime import datetime, timezone
from models import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-password_hash', '-favorites.user', '-favorites.recipe', '-shopping_list.user', '-recipes.users')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")  # Role can be 'admin' or 'user'
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Relationships
    favorites = db.relationship('Favorite', back_populates='user', lazy=True)
    #shopping_list = db.relationship('ShoppingList', backref='user', lazy=True)
    #recipes = db.relationship('Recipe', backref='creator', lazy=True)

    # Password hashing and checking methods
    def set_password(self, password):
        """Hash the user's password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the password."""
        return check_password_hash(self.password_hash, password)