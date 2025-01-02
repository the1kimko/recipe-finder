from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# Naming convention for foreign keys and other constraints
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initialize SQLAlchemy with metadata
db = SQLAlchemy(metadata=metadata)

from models.favorite import Favorite
from models.shopping_list import ShoppingList
from models.user import User