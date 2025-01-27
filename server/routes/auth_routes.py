from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from models.user import User, db
import cloudinary.uploader

auth_bp = Blueprint('auth', __name__)

# User Registration
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.form.to_dict()  # Use form data for text fields
    file = request.files.get('file')  # Get the file from the request (if provided)

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')  # Default role is 'user'

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    # Upload profile picture to Cloudinary (if provided)
    image_url = "https://example.com/default-profile.png"  # Default image
    if file:
        try:
            upload_result = cloudinary.uploader.upload(file)
            image_url = upload_result.get('secure_url')
        except Exception as e:
            return jsonify({"error": f"Failed to upload image: {str(e)}"}), 500
    
    # Create new user
    user = User(username=username, email=email, role=role, image_url=image_url)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# User Login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    # Create JWT
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role}
    )
    return jsonify({"access_token": access_token, "role": user.role}), 200

# Verify Admin Role
@auth_bp.route('/verify-admin', methods=['GET'])
@jwt_required()
def verify_admin():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403
    return jsonify({"message": "Admin access verified"}), 200


