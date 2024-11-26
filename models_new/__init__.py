from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy extension
db = SQLAlchemy()

# Import all models to make them available for the application
from .author_model import Author
from .book_model import Book
from .cart_items_model import CartItem
from .category_model import Category
from .order_model import Order, OrderDetail
from .user_model import User
