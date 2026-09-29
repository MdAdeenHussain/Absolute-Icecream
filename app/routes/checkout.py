import secrets
from decimal import Decimal

from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from app.extensions import db
from app.models.order import Order, OrderItem
from app.models.product import ProductVariant
from app.services.cart_service import CartService
from app.utils.auth import current_customer

checkout_bp = Blueprint(
    "checkout",
    __name__,
    url_prefix=""
)


def generate_order_number():

    return (
        "AI-"
        + secrets.token_hex(5).upper()
    )


@checkout_bp.route("/checkout")
def checkout_page():

    cart = CartService.hydrate(session)

    if not cart["items"]:
        return redirect(
            url_for("cart.cart_page")
        )

    return render_template(
        "checkout.html",
        cart=cart
    )


@checkout_bp.get("/checkout/payment/<int:order_id>")
def payment_page(order_id):
    """Show a pending payment state until a configured provider confirms it."""
    order = db.session.get(Order, order_id)
    if order is None:
        return redirect(url_for("cart.cart_page"))
    return render_template("payment.html", order=order)


@checkout_bp.post("/api/checkout/create")
def create_order():

    data = request.get_json(
        silent=True
    ) or {}

    customer = current_customer()

    required = [
        "name",
        "email",
        "phone",
        "address_line_1",
        "city",
        "state",
        "postal_code"
    ]

    missing = [
        field
        for field in required
        if not str(
            data.get(field, "")
        ).strip()
    ]

    if missing:

        return jsonify({
            "error":
                "Please complete all required fields.",
            "fields": missing
        }), 400


    cart = CartService.hydrate(session)

    if not cart["items"]:

        return jsonify({
            "error": "Your cart is empty."
        }), 400


    # Re-check stock from database immediately
    # before creating the order.

    for item in cart["items"]:

        variant = db.session.get(ProductVariant, item["variant_id"])

        if not variant:

            return jsonify({
                "error":
                    "One of the products is no longer available."
            }), 409

        if (
            variant.stock_quantity
            < item["quantity"]
        ):

            return jsonify({
                "error":
                    f"{variant.product.name} "
                    "does not have enough stock."
            }), 409


    subtotal = Decimal(
        str(cart["subtotal"])
    )

    shipping_fee = Decimal("0.00")

    discount = Decimal("0.00")

    total = (
        subtotal
        + shipping_fee
        - discount
    )


    order = Order(

        order_number=
            generate_order_number(),

        status="pending",

        payment_status="pending",

        subtotal=subtotal,

        shipping_amount=shipping_fee,

        discount_amount=discount,

        total_amount=total,

        customer_id=
            customer.id
            if customer else None,
        
        notes=(
            f"Checkout contact: {data['name'].strip()} <{data['email'].strip().lower()}>; "
            f"{data['phone'].strip()}; {data['address_line_1'].strip()}, "
            f"{data['city'].strip()}, {data['state'].strip()} {data['postal_code'].strip()}"
        )

    )

    db.session.add(order)

    for item in cart["items"]:

        variant = db.session.get(ProductVariant, item["variant_id"])

        order_item = OrderItem(

            order=order,

            variant_id=variant.id,

            product_id=variant.product_id,

            product_name=
                variant.product.name,

            variant_name=variant.name,

            unit_price=
                variant.price,

            quantity=
                item["quantity"],

            total_price=
                variant.price
                * item["quantity"]

        )

        db.session.add(order_item)


    db.session.commit()


    session["pending_order_id"] = order.id

    return jsonify({
        "success": True,

        "order_number":
            order.order_number,

        "order_id":
            order.id,

        "total":
            float(order.total_amount),

        "payment_required":
            True,

        "payment_provider":
            None

    })
    
