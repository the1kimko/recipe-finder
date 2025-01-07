from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User, db

user_bp = Blueprint('users', __name__)

# Admin: Get all users
@user_bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    identity = get_jwt_identity()
    if identity["role"] != "admin":
        return jsonify({"error": "Admin access required"}), 403

    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

# Get current user
@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()["id"]
    user = User.query.get(user_id)
    return jsonify(user.to_dict()), 200

# Update user (self or admin)
@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    identity = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Allow only admins or the user to update the profile
    if identity["id"] != user_id and identity["role"] != "admin":
        return jsonify({"error": "Unauthorized access"}), 403

    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role) if identity["role"] == "admin" else user.role
    db.session.commit()

    return jsonify({"message": "User updated successfully"}), 200

# Delete user (self or admin)
@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    identity = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Allow only admins or the user to delete the account
    if identity["id"] != user_id and identity["role"] != "admin":
        return jsonify({"error": "Unauthorized access"}), 403

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User deleted successfully"}), 200
