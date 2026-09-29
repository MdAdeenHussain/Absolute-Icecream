from datetime import datetime

from app.extensions import db


class Flavor(db.Model):
    """Ice cream flavor."""

    __tablename__ = "flavors"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
    )

    slug = db.Column(
        db.String(140),
        unique=True,
        nullable=False,
    )

    description = db.Column(
        db.Text,
    )

    accent_color = db.Column(
        db.String(20),
        nullable=False,
        default="#071522",
    )

    launch_status = db.Column(
        db.String(30),
        nullable=False,
        default="coming_soon",
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    products = db.relationship(
        "Product",
        back_populates="flavor",
    )