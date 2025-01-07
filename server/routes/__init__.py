from .auth_routes import auth_bp
from .favorite_routes import favorite_bp
from .shopping_list_routes import shopping_list_bp
from .user_routes import user_bp

# Function to register all blueprints
def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(favorite_bp, url_prefix="/favorites")
    app.register_blueprint(shopping_list_bp, url_prefix="/shopping_lists")
    app.register_blueprint(user_bp, url_prefix="/users")