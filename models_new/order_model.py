from . import db
from sqlalchemy.schema import Sequence
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'Orders'  # table name with a capatalized convention
    order_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    # Relationships
    details = db.relationship('OrderDetail', back_populates='order', cascade="all, delete-orphan")

  # String representation
    def __repr__(self):
        return f"<Order {self.order_id}, User {self.user_id}, Total {self.total_price}>"
    

class OrderDetail(db.Model):
    __tablename__ = 'order_details'
    order_details_id = db.Column(
        db.Integer, 
        Sequence('order_details_id_seq', start=1, increment=1), 
        primary_key=True
    )
    order_id = db.Column(db.Integer, db.ForeignKey('Orders.order_id'), nullable=False)  # Référence à 'Orders' avec majuscule
    book_id = db.Column(db.Integer, db.ForeignKey('Book.book_id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

    # Relationships
    order = db.relationship('Order', back_populates='details')
    book = db.relationship('Book')

   # String representation
    def __repr__(self):
        return f"<OrderDetail {self.order_details_id}, Order {self.order_id}, Book {self.book_id}>"
