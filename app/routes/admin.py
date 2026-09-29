from datetime import datetime

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app.extensions import db
from app.models.admin import Admin
from app.models.customer import Customer
from app.models.order import Order
from app.models.product import Product
from app.utils.admin_auth import (
    admin_required,
    current_admin,
    login_admin,
    logout_admin,
)

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = (
            request.form
            .get("email", "")
            .strip()
            .lower()
        )

        password = request.form.get(
            "password",
            ""
        )

        admin = Admin.query.filter_by(
            email=email
        ).first()

        if (
            not admin
            or not admin.is_active
            or not admin.check_password(password)
        ):

            flash(
                "Invalid administrator credentials.",
                "error"
            )

            return redirect(
                url_for("admin.login")
            )

        login_admin(admin)

        admin.last_login_at = datetime.utcnow()

        db.session.commit()

        return redirect(
            url_for("admin.dashboard")
        )

    return render_template(
        "admin/login.html"
    )


@admin_bp.route("/logout")
def logout():

    logout_admin()

    return redirect(
        url_for("admin.login")
    )


@admin_bp.route("/")
@admin_required
def dashboard():

    products_count = Product.query.count()

    customers_count = Customer.query.count()

    orders_count = Order.query.count()

    pending_orders = Order.query.filter(
        Order.status.in_([
            "pending",
            "confirmed",
            "processing"
        ])
    ).count()

    recent_orders = Order.query.order_by(
        Order.created_at.desc()
    ).limit(10).all()

    total_revenue = db.session.query(
        db.func.coalesce(
            db.func.sum(Order.total_amount),
            0
        )
    ).filter(
        Order.payment_status == "paid"
    ).scalar()

    return render_template(
        "admin/dashboard.html",
        admin=current_admin(),
        products_count=products_count,
        customers_count=customers_count,
        orders_count=orders_count,
        pending_orders=pending_orders,
        total_revenue=total_revenue,
        recent_orders=recent_orders
    )

@admin_bp.route("/products")
@admin_required
def products():

    products = Product.query.order_by(
        Product.created_at.desc()
    ).all()

    return render_template(
        "admin/products.html",
        admin=current_admin(),
        products=products
    )

@admin_bp.route("/orders")
@admin_required
def orders():

    orders = Order.query.order_by(
        Order.created_at.desc()
    ).all()

    return render_template(
        "admin/orders.html",
        admin=current_admin(),
        orders=orders
    )

@admin_bp.route("/customers")
@admin_required
def customers():

    customers = Customer.query.order_by(
        Customer.created_at.desc()
    ).all()

    return render_template(
        "admin/customers.html",
        admin=current_admin(),
        customers=customers
    )

