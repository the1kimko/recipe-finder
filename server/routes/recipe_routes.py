from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.recipe import Recipe, db
import random

recipes_bp = Blueprint('recipes', __name__)

# Fetch all recipes (Public)
@recipes_bp.route('', methods=['GET'])
def get_all_recipes():
    recipes = Recipe.query.all()
    print([recipe.favorites for recipe in recipes])
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
    claims = get_jwt()
    role = claims.get("role")

    if role != "admin":
        return jsonify({"error": "Admin access required"}), 403

    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"message": "Recipe deleted successfully"}), 200

# Admin: Add custom recipe
@recipes_bp.route('/', methods=['POST'])
@jwt_required()
def add_recipe():
    # Get user ID from the token identity
    user_id = get_jwt_identity()
    # Get additional claims from the token
    claims = get_jwt()
    role = claims.get("role")

    if role != "admin":
        return jsonify({"error": "Admin access required"}), 403

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400
    
    spoonacular_id = data.get("spoonacular_id", random.randint(100000, 999999))
    title = data.get("title")
    description = data.get("description")
    ingredients = data.get("ingredients")
    instructions = data.get("instructions")
    image_url = data.get("image_url", "https://example.com/default-recipe.png")
    source_url = data.get("source_url", None)
    ready_in_minutes = data.get("ready_in_minutes", None)
    servings = data.get("servings", None)

    if not title or not ingredients or not instructions:
        return jsonify({"error": "Title, ingredients, and instructions are required"}), 400

    new_recipe = Recipe(
        spoonacular_id=spoonacular_id,
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

# Admin: Update Recipe
@recipes_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_recipe(id):
    claims = get_jwt()
    role = claims.get("role")

    if role != "admin":
        return jsonify({"error": "Admin access required"}), 403

    recipe = Recipe.query.get(id)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    recipe.title = data.get("title", recipe.title)
    recipe.description = data.get("description", recipe.description)
    recipe.ingredients = data.get("ingredients", recipe.ingredients)
    recipe.instructions = data.get("instructions", recipe.instructions)
    recipe.image_url = data.get("image_url", recipe.image_url)
    recipe.source_url = data.get("source_url", recipe.source_url)
    recipe.ready_in_minutes = data.get("ready_in_minutes", recipe.ready_in_minutes)
    recipe.servings = data.get("servings", recipe.servings)

    db.session.commit()
    return jsonify({"message": "Recipe updated successfully", "recipe": recipe.to_dict()}), 200

@recipes_bp.route('/debug-token', methods=['GET'])
@jwt_required()
def debug_token():
    identity = get_jwt_identity()
    claims = get_jwt()
    print(f"Identity: {identity}, Claims: {claims}")
    return jsonify({"identity": identity, "claims": claims}), 200
