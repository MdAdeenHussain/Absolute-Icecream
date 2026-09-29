from functools import wraps

from flask import (
    redirect,
    request,
    session,
    url_for,
)

from app.models.customer import Customer
from app.extensions import db


SESSION_KEY = "customer_id"


def login_customer(customer):
    session.clear()
    session[SESSION_KEY] = customer.id


def logout_customer():
    session.pop(SESSION_KEY, None)


def current_customer():
    customer_id = session.get(SESSION_KEY)

    if not customer_id:
        return None

    return db.session.get(Customer, customer_id)


def customer_logged_in():
    return current_customer() is not None


def customer_required(view):

    @wraps(view)
    def wrapped(*args, **kwargs):

        if not current_customer():

            return redirect(
                url_for(
                    "auth.login",
                    next=request.full_path
                )
            )

        return view(*args, **kwargs)

    return wrapped
