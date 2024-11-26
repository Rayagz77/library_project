# models/cart_model.py
from . import db

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    cart_item_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('Book.book_id'), nullable=False)

    # Relationships 
    user = db.relationship('User', back_populates='cart_items')  # Bidirectional relationship with User
    book = db.relationship('Book', back_populates='cart_items')  # Bidirectional relationship  with Book

# String representation
    def __repr__(self):
        return f"<CartItem {self.cart_item_id} - User {self.user_id}, Book {self.book_id}>"
