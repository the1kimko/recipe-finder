from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.shopping_list import ShoppingList, db

shopping_list_bp = Blueprint('shopping_list', __name__)

# Add Shopping List Item
@shopping_list_bp.route('/', methods=['POST'])
@jwt_required()
def add_shopping_item():
    data = request.get_json()
    user_id = get_jwt_identity()["id"]

    item_name = data.get('item_name')
    recipe_id = data.get('recipe_id')
    amount = data.get('amount', None)
    unit = data.get('unit', None)

    if not item_name or not recipe_id:
        return jsonify({"error": "Item name is or recipe ID required"}), 400

    item = ShoppingList(user_id=user_id, recipe_id=recipe_id, item_name=item_name, amount=amount, unit=unit)
    db.session.add(item)
    db.session.commit()

    return jsonify({"message": "Item added to shopping list"}), 201

# Get Shopping List
@shopping_list_bp.route('/', methods=['GET'])
@jwt_required()
def get_shopping_list():
    user_id = get_jwt_identity()["id"]
    items = ShoppingList.query.filter_by(user_id=user_id).all()
    return jsonify([item.to_dict() for item in items]), 200

# Delete Shopping List Item
@shopping_list_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_shopping_item(id):
    user_id = get_jwt_identity()["id"]
    item = ShoppingList.query.filter_by(id=id, user_id=user_id).first()

    if not item:
        return jsonify({"error": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted"}), 200
