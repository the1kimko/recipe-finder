from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.favorite import Favorite, db

favorite_bp = Blueprint('favorites', __name__)

# Create Favorite
@favorite_bp.route('/', methods=['POST'])
@jwt_required()
def add_favorite():
    data = request.get_json()
    user_id = get_jwt_identity()

    recipe_id = data.get('recipe_id')
    recipe_title = data.get('recipe_title')

    if not recipe_id or not recipe_title:
        return jsonify({"error": "Recipe ID and title are required"}), 400

    try:
        favorite = Favorite(user_id=user_id, recipe_id=recipe_id, recipe_title=recipe_title)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite added"}), 201
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Read Favorites
@favorite_bp.route('/', methods=['GET'])
@jwt_required()
def get_favorites():
    user_id = get_jwt_identity()
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([fav.to_dict() for fav in favorites]), 200

# Delete Favorite
@favorite_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_favorite(id):
    user_id = get_jwt_identity()
    favorite = Favorite.query.filter_by(id=id, user_id=user_id).first()

    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite deleted"}), 200
