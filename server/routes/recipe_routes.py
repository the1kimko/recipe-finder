from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.recipe import Recipe, db

recipes_bp = Blueprint('recipes', __name__)

# Fetch all recipes (Public)
@recipes_bp.route('/', methods=['GET'])
def get_all_recipes():
    recipes = Recipe.query.all()
    return jsonify([recipe.to_dict() for recipe in recipes]), 200

# Fetch recipe by ID (Public)
@recipes_bp.route('/<int:recipe_id>', methods=['GET'])
def get_recipe_by_id(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404
    return jsonify(recipe.to_dict()), 200

# Admin: Delete recipe by ID
@recipes_bp.route('/<int:recipe_id>', methods=['DELETE'])
@jwt_required()
def delete_recipe(recipe_id):
    identity = get_jwt_identity()
    if identity["role"] != "admin":
        return jsonify({"error": "Admin access required"}), 403

    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"message": "Recipe deleted successfully"}), 200

# Admin: Add custom recipe
@recipes_bp.route('/', methods=['POST'])
@jwt_required()
def add_recipe():
    identity = get_jwt_identity()
    if identity["role"] != "admin":
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    ingredients = data.get("ingredients")  # Comma-separated string
    instructions = data.get("instructions")
    image_url = data.get("image_url", "https://example.com/default-recipe.png")
    source_url = data.get("source_url", None)
    ready_in_minutes = data.get("ready_in_minutes", None)
    servings = data.get("servings", None)

    if not title or not ingredients or not instructions:
        return jsonify({"error": "Title, ingredients, and instructions are required"}), 400

    new_recipe = Recipe(
        title=title,
        description=description,
        ingredients=ingredients,
        instructions=instructions,
        image_url=image_url,
        source_url=source_url,
        ready_in_minutes=ready_in_minutes,
        servings=servings
    )

    db.session.add(new_recipe)
    db.session.commit()

    return jsonify({"message": "Recipe added successfully", "recipe": new_recipe.to_dict()}), 201
