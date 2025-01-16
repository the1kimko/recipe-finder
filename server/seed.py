from models import db
from models.user import User
from models.favorite import Favorite
from models.shopping_list import ShoppingList
from models.recipe import Recipe
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

        # Add Recipes
        recipe1 = Recipe(
            id=101,
            spoonacular_id=1001,  # Dummy spoonacular_id
            title="Spaghetti Carbonara",
            description="A classic Italian pasta dish made with eggs, cheese, pancetta, and pepper.",
            ingredients="Spaghetti, Eggs, Pancetta, Parmesan Cheese, Black Pepper",
            instructions="1. Boil spaghetti. 2. Cook pancetta. 3. Mix eggs and cheese. 4. Combine all ingredients.",
            image_url="https://example.com/spaghetti-carbonara.jpg",
            source_url="https://example.com/spaghetti-carbonara",
            ready_in_minutes=30,
            servings=2,
        )
        recipe2 = Recipe(
            id=102,
            spoonacular_id=1002,  # Dummy spoonacular_id
            title="Vegetarian Pizza",
            description="A delicious vegetarian pizza topped with fresh vegetables and mozzarella cheese.",
            ingredients="Pizza Dough, Tomato Sauce, Mozzarella Cheese, Bell Peppers, Onions, Mushrooms",
            instructions="1. Prepare dough. 2. Add toppings. 3. Bake in oven at 220°C for 15 minutes.",
            image_url="https://example.com/vegetarian-pizza.jpg",
            source_url="https://example.com/vegetarian-pizza",
            ready_in_minutes=20,
            servings=4,
        )

        db.session.add_all([recipe1, recipe2])

        # Add Favorites
        favorite1 = Favorite(user_id=1, recipe_id=101, recipe_title=recipe1.title)
        favorite2 = Favorite(user_id=2, recipe_id=102, recipe_title=recipe2.title)
        db.session.add_all([favorite1, favorite2])

        # Add Shopping List Items
        item1 = ShoppingList(user_id=1, recipe_id=101, item_name="Pancetta")
        item2 = ShoppingList(user_id=2, recipe_id=102, item_name="Mozzarella Cheese")
        db.session.add_all([item1, item2])

        # Commit to the database
        db.session.commit()
        print("Database seeded successfully!")

# Run seed function
if __name__ == "__main__":
    seed()

