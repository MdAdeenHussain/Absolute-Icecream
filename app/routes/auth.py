from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app.extensions import db
from app.models.customer import Customer
from app.services.auth_service import normalize_email
from app.utils.auth import (
    login_customer,
    logout_customer,
)


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/account"
)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        first_name = request.form.get(
            "first_name",
            ""
        ).strip()

        last_name = request.form.get(
            "last_name",
            ""
        ).strip()

        email = normalize_email(
            request.form.get("email")
        )

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if not first_name:
            flash(
                "Please enter your first name.",
                "error"
            )
            return redirect(
                url_for("auth.register")
            )

        if not email:
            flash(
                "Please enter your email address.",
                "error"
            )
            return redirect(
                url_for("auth.register")
            )

        if len(password) < 8:
            flash(
                "Password must contain at least 8 characters.",
                "error"
            )
            return redirect(
                url_for("auth.register")
            )

        if password != confirm_password:
            flash(
                "Passwords do not match.",
                "error"
            )
            return redirect(
                url_for("auth.register")
            )

        existing = Customer.query.filter_by(
            email=email
        ).first()

        if existing:
            flash(
                "An account with this email already exists.",
                "error"
            )
            return redirect(
                url_for("auth.login")
            )

        customer = Customer(
            first_name=first_name,
            last_name=last_name or None,
            email=email,
            phone=phone or None
        )

        customer.set_password(password)

        db.session.add(customer)
        db.session.commit()

        login_customer(customer)

        return redirect(
            url_for("account.dashboard")
        )

    return render_template(
        "auth/register.html"
    )


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = normalize_email(
            request.form.get("email")
        )

        password = request.form.get(
            "password",
            ""
        )

        customer = Customer.query.filter_by(
            email=email
        ).first()

        if not customer or not customer.check_password(
            password
        ):
            flash(
                "Invalid email or password.",
                "error"
            )

            return redirect(
                url_for("auth.login")
            )

        if not customer.is_active:
            flash(
                "This account is currently unavailable.",
                "error"
            )

            return redirect(
                url_for("auth.login")
            )

        login_customer(customer)

        next_url = request.args.get("next")

        if next_url and next_url.startswith("/"):
            return redirect(next_url)

        return redirect(
            url_for("account.dashboard")
        )

    return render_template(
        "auth/login.html"
    )


@auth_bp.route("/logout")
def logout():

    logout_customer()

    return redirect(
        url_for("shop.shop")
    )