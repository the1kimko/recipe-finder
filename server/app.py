from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from models import db
from routes import register_blueprints
import os
from dotenv import load_dotenv
import cloudinary

# Load environment variables from .env file
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# Configure the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipe_finder.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['JWT_SECRET_KEY'] = 'your_secret_key'

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default_secret_key')

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

# Initialize database and migration
db.init_app(app)
migrate = Migrate(app, db)

# Initialize JWT manager
jwt = JWTManager(app)

# Register blueprints
register_blueprints(app)

if __name__ == '__main__':
    app.run(port=5555, debug=True)