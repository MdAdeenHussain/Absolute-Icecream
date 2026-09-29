import os

from app.extensions import db
from app.models.admin import Admin


def create_initial_admin():

    email = os.getenv(
        "ADMIN_EMAIL"
    )

    password = os.getenv(
        "ADMIN_PASSWORD"
    )

    name = os.getenv(
        "ADMIN_NAME",
        "Absolute Icecream Admin"
    )

    if not email or not password:
        return

    existing = Admin.query.filter_by(
        email=email.lower()
    ).first()

    if existing:
        return

    admin = Admin(
        name=name,
        email=email.lower(),
        role="admin"
    )

    admin.set_password(password)

    db.session.add(admin)
    db.session.commit()