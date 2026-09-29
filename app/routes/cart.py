from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
    session
)

from app.extensions import db
from app.models.product import ProductVariant
from app.services.cart_service import CartService


cart_bp = Blueprint(
    "cart",
    __name__
)


def cart_response():

    return jsonify(
        CartService.hydrate(session)
    )


@cart_bp.route("/cart")
def cart_page():

    cart = CartService.hydrate(session)

    return render_template(
        "cart.html",
        cart=cart
    )


@cart_bp.get("/api/cart")
def get_cart():
    return cart_response()


@cart_bp.post("/api/cart/add")
def add_to_cart():

    data = request.get_json(
        silent=True
    ) or {}

    variant_id = data.get("variant_id")
    quantity = data.get("quantity", 1)

    try:
        variant_id = int(variant_id)
        quantity = int(quantity)
    except (
        TypeError,
        ValueError
    ):
        return jsonify({
            "error": "Invalid cart data."
        }), 400

    if quantity < 1:
        return jsonify({
            "error": "Quantity must be at least 1."
        }), 400

    variant = db.session.get(ProductVariant, variant_id)

    if not variant or not variant.is_active:
        return jsonify({
            "error": "Product variant not found."
        }), 404

    if variant.stock_quantity <= 0:
        return jsonify({
            "error": "This item is currently unavailable."
        }), 409

    cart = CartService.get_cart(session)

    current_quantity = int(
        cart.get(str(variant_id), 0)
    )

    if current_quantity + quantity > variant.stock_quantity:

        return jsonify({
            "error": "Requested quantity exceeds available stock."
        }), 409

    CartService.add(
        session,
        variant_id,
        quantity
    )

    return cart_response()


@cart_bp.patch("/api/cart/update")
def update_cart():

    data = request.get_json(
        silent=True
    ) or {}

    try:
        variant_id = int(
            data.get("variant_id")
        )

        quantity = int(
            data.get("quantity")
        )

    except (
        TypeError,
        ValueError
    ):
        return jsonify({
            "error": "Invalid cart data."
        }), 400

    variant = db.session.get(ProductVariant, variant_id)

    if not variant:
        return jsonify({
            "error": "Product variant not found."
        }), 404

    if quantity > variant.stock_quantity:

        return jsonify({
            "error": "Requested quantity exceeds available stock."
        }), 409

    CartService.update(
        session,
        variant_id,
        quantity
    )

    return cart_response()


@cart_bp.delete("/api/cart/remove/<int:variant_id>")
def remove_from_cart(variant_id):

    CartService.remove(
        session,
        variant_id
    )

    return cart_response()


@cart_bp.post("/api/cart/clear")
def clear_cart():

    CartService.clear(session)

    return cart_response()
