from functools import wraps

from flask import (
    redirect,
    session,
    url_for,
)

from app.models.admin import Admin
from app.extensions import db


ADMIN_SESSION_KEY = "admin_id"


def login_admin(admin):

    session[ADMIN_SESSION_KEY] = admin.id
    session["is_admin"] = True


def logout_admin():

    session.pop(ADMIN_SESSION_KEY, None)
    session.pop("is_admin", None)


def current_admin():

    admin_id = session.get(
        ADMIN_SESSION_KEY
    )

    if not admin_id:
        return None

    return db.session.get(Admin, admin_id)


def admin_required(view):

    @wraps(view)
    def wrapped(*args, **kwargs):

        admin = current_admin()

        if not admin or not admin.is_active:

            return redirect(
                url_for("admin.login")
            )

        return view(*args, **kwargs)

    return wrapped
