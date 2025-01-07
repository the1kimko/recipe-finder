from models import db
from models.user import User
from models.favorite import Favorite
from models.shopping_list import ShoppingList
from app import app

# Seed Data
def seed():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Add Users
        user1 = User(username="admin", email="admin@example.com", role="admin")
        user1.set_password("admin123")
        user2 = User(username="user", email="user@example.com", role="user")
        user2.set_password("user123")

        db.session.add_all([user1, user2])

        # Add Favorites
        favorite1 = Favorite(user_id=1, recipe_id=101, recipe_title="Spaghetti Carbonara")
        favorite2 = Favorite(user_id=2, recipe_id=102, recipe_title="Vegetarian Pizza")
        db.session.add_all([favorite1, favorite2])

        # Add Shopping List Items
        item1 = ShoppingList(user_id=1, item_name="Tomatoes")
        item2 = ShoppingList(user_id=2, item_name="Mozzarella Cheese")
        db.session.add_all([item1, item2])

        # Commit to the database
        db.session.commit()
        print("Database seeded successfully!")

# Run seed function
if __name__ == "__main__":
    seed()
