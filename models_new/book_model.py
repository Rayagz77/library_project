# models/book_model.py
from . import db
from models_new.author_model import Author
from models_new.category_model import Category

class Book(db.Model):
    __tablename__ = 'Book'
    book_id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String(255), nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    book_price = db.Column(db.Float, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('Author.author_id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('Category.category_id'), nullable=False)
    book_image_url = db.Column(db.String, nullable=True)

    # Relations
    author = db.relationship('Author', backref='books')
    category = db.relationship('Category', backref='books')
    cart_items = db.relationship('CartItem', back_populates='book')  # Modifiez le back_populates si nécessaire

    def __repr__(self):
        return f"<Book {self.book_title}>"
