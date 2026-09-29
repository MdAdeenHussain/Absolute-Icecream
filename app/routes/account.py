from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app.extensions import db
from app.models.customer_address import CustomerAddress
from app.utils.auth import (
    current_customer,
    customer_required,
)


account_bp = Blueprint(
    "account",
    __name__,
    url_prefix="/account"
)


@account_bp.route("/")
@customer_required
def dashboard():

    customer = current_customer()

    orders = sorted(
        customer.orders,
        key=lambda order: order.created_at,
        reverse=True
    )

    return render_template(
        "account/dashboard.html",
        customer=customer,
        orders=orders[:5]
    )


@account_bp.route("/profile", methods=["GET", "POST"])
@customer_required
def profile():

    customer = current_customer()

    if request.method == "POST":

        customer.first_name = request.form.get(
            "first_name",
            ""
        ).strip()

        customer.last_name = request.form.get(
            "last_name",
            ""
        ).strip() or None

        customer.phone = request.form.get(
            "phone",
            ""
        ).strip() or None

        db.session.commit()

        flash(
            "Your profile has been updated.",
            "success"
        )

        return redirect(
            url_for("account.profile")
        )

    return render_template(
        "account/profile.html",
        customer=customer
    )


@account_bp.route("/addresses")
@customer_required
def addresses():

    customer = current_customer()

    return render_template(
        "account/addresses.html",
        customer=customer,
        addresses=customer.addresses
    )


@account_bp.route(
    "/addresses/add",
    methods=["GET", "POST"]
)
@customer_required
def add_address():

    customer = current_customer()

    if request.method == "POST":

        address = CustomerAddress(
            customer_id=customer.id,

            label=request.form.get(
                "label",
                ""
            ).strip() or None,

            recipient_name=request.form.get(
                "recipient_name",
                ""
            ).strip(),

            phone=request.form.get(
                "phone",
                ""
            ).strip(),

            address_line_1=request.form.get(
                "address_line_1",
                ""
            ).strip(),

            address_line_2=request.form.get(
                "address_line_2",
                ""
            ).strip() or None,

            city=request.form.get(
                "city",
                ""
            ).strip(),

            state=request.form.get(
                "state",
                ""
            ).strip(),

            postal_code=request.form.get(
                "postal_code",
                ""
            ).strip(),

            country=request.form.get(
                "country",
                "India"
            ).strip() or "India",

            is_default=bool(
                request.form.get("is_default")
            )
        )

        if address.is_default:

            CustomerAddress.query.filter_by(
                customer_id=customer.id
            ).update({
                "is_default": False
            })

        db.session.add(address)
        db.session.commit()

        flash(
            "Address saved.",
            "success"
        )

        return redirect(
            url_for("account.addresses")
        )

    return render_template(
        "account/address_form.html"
    )


@account_bp.route(
    "/addresses/<int:address_id>/delete",
    methods=["POST"]
)
@customer_required
def delete_address(address_id):

    customer = current_customer()

    address = CustomerAddress.query.filter_by(
        id=address_id,
        customer_id=customer.id
    ).first_or_404()

    db.session.delete(address)
    db.session.commit()

    flash(
        "Address removed.",
        "success"
    )

    return redirect(
        url_for("account.addresses")
    )


@account_bp.route("/orders")
@customer_required
def orders():

    customer = current_customer()

    orders = sorted(
        customer.orders,
        key=lambda order: order.created_at,
        reverse=True
    )

    return render_template(
        "account/orders.html",
        customer=customer,
        orders=orders
    )


@account_bp.route(
    "/orders/<int:order_id>"
)
@customer_required
def order_detail(order_id):

    customer = current_customer()

    order = next(
        (
            order
            for order in customer.orders
            if order.id == order_id
        ),
        None
    )

    if not order:
        return redirect(
            url_for("account.orders")
        )

    return render_template(
        "account/order_detail.html",
        order=order
    )