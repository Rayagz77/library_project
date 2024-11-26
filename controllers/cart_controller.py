from flask import Blueprint, session, flash, redirect, url_for, render_template
from models_new import db, CartItem, Order, OrderDetail
from datetime import datetime

cart_bp = Blueprint('cart_bp', __name__)

@cart_bp.route('/add/<int:book_id>', methods=['POST'])
def add_to_cart(book_id):
    user_id = session.get('user_id')
    if not user_id:
        flash("Veuillez vous connecter pour ajouter des articles au panier.", "warning")
        return redirect(url_for('auth.login'))  # Adjusted to match typical auth route

    # Ensure book_id is valid and prevent duplicates
    try:
        existing_item = CartItem.query.filter_by(user_id=user_id, book_id=book_id).first()
        if existing_item:
            flash("Ce livre est déjà dans votre panier.", "info")
        else:
            new_item = CartItem(user_id=user_id, book_id=book_id)
            db.session.add(new_item)
            db.session.commit()
            flash("Livre ajouté au panier avec succès.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de l'ajout au panier : {str(e)}", "danger")

    return redirect(url_for('home'))

@cart_bp.route('/remove/<int:cart_item_id>', methods=['POST'])
def remove_from_cart(cart_item_id):
    user_id = session.get('user_id')
    if not user_id:
        flash("Veuillez vous connecter pour gérer votre panier.", "warning")
        return redirect(url_for('auth.login'))

    # Ensure the cart item belongs to the user
    cart_item = CartItem.query.filter_by(cart_item_id=cart_item_id, user_id=user_id).first()
    if cart_item:
        try:
            db.session.delete(cart_item)
            db.session.commit()
            flash("Article retiré du panier avec succès.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de la suppression de l'article : {str(e)}", "danger")
    else:
        flash("Article introuvable ou non autorisé.", "danger")

    return redirect(url_for('cart_bp.view_cart'))

@cart_bp.route('/', methods=['GET'])
def view_cart():
    user_id = session.get('user_id')
    if not user_id:
        flash("Veuillez vous connecter pour voir votre panier.", "warning")
        return redirect(url_for('auth.login'))

    # Fetch cart items and calculate total price
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    total_price = sum(item.book.book_price for item in cart_items if item.book)

    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@cart_bp.route('/validate', methods=['POST'])
def validate_cart():
    user_id = session.get('user_id')
    if not user_id:
        flash("Veuillez vous connecter pour valider votre panier.", "warning")
        return redirect(url_for('auth.login'))

    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        flash("Votre panier est vide.", "info")
        return redirect(url_for('cart_bp.view_cart'))

    try:
        # Create a new order
        order = Order(user_id=user_id, order_date=datetime.utcnow(), total_price=0)
        db.session.add(order)
        db.session.flush()  # Ensure order_id is available

        # Add order details
        total_price = 0
        for item in cart_items:
            if not item.book:
                continue  # Skip items with missing books
            order_detail = OrderDetail(
                order_id=order.order_id,
                book_id=item.book_id,
                quantity=1,
                unit_price=item.book.book_price
            )
            db.session.add(order_detail)
            total_price += item.book.book_price

        # Update total price in the order
        order.total_price = total_price

        # Clear the cart
        CartItem.query.filter_by(user_id=user_id).delete()

        db.session.commit()
        flash("Commande validée avec succès.", "success")
        return redirect(url_for('cart_bp.order_confirmation', order_id=order.order_id))
    except Exception as e:
        db.session.rollback()
        flash(f"Erreur lors de la validation de la commande : {str(e)}", "danger")
        return redirect(url_for('cart_bp.view_cart'))

@cart_bp.route('/confirmation/<int:order_id>', methods=['GET'])
def order_confirmation(order_id):
    user_id = session.get('user_id')
    if not user_id:
        flash("Veuillez vous connecter pour voir votre commande.", "warning")
        return redirect(url_for('auth.login'))

    order = Order.query.filter_by(order_id=order_id, user_id=user_id).first()
    if not order:
        flash("Commande introuvable ou non autorisée.", "danger")
        return redirect(url_for('home'))

    return render_template('order_confirmation.html', order=order)

# Inject cart count into templates
@cart_bp.context_processor
def inject_cart_count():
    user_id = session.get('user_id')
    cart_count = 0
    if user_id:
        cart_count = CartItem.query.filter_by(user_id=user_id).count()
    return {'cart_count': cart_count}

