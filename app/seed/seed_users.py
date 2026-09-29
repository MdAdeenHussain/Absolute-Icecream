import sys

from app import create_app
from app.extensions import db
from app.models import Role, User


ROLES = [
    {
        "name": "customer",
        "description": "Standard customer account.",
    },
    {
        "name": "admin",
        "description": "Absolute Icecream administrator.",
    },
]


def seed_users():
    """Create initial roles and development admin."""

    app = create_app("development")

    with app.app_context():

        for role_data in ROLES:

            role = Role.query.filter_by(
                name=role_data["name"]
            ).first()

            if role is None:

                role = Role(
                    name=role_data["name"],
                    description=role_data[
                        "description"
                    ],
                )

                db.session.add(role)

        db.session.commit()

        admin_email = "admin@absoluteicecream.local"

        admin = User.query.filter_by(
            email=admin_email
        ).first()

        if admin is None:

            admin = User(
                email=admin_email,
                first_name="Absolute",
                last_name="Admin",
                email_verified=True,
            )

            admin.set_password(
                "ChangeMeImmediately123!"
            )

            admin_role = Role.query.filter_by(
                name="admin"
            ).first()

            admin.roles.append(admin_role)

            db.session.add(admin)

        db.session.commit()

        print(
            "Development admin created:"
        )
        print(
            f"Email: {admin_email}"
        )
        print(
            "Password: ChangeMeImmediately123!"
        )
        print(
            "Change this password before any "
            "non-development deployment."
        )


if __name__ == "__main__":
    try:
        seed_users()
    except Exception as exc:
        print(
            f"User seed failed: {exc}",
            file=sys.stderr,
        )
        raise