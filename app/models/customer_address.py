from datetime import datetime

from app.extensions import db


class CustomerAddress(db.Model):
    __tablename__ = "customer_addresses"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=False,
        index=True
    )

    label = db.Column(
        db.String(50),
        nullable=True
    )

    recipient_name = db.Column(
        db.String(150),
        nullable=False
    )

    phone = db.Column(
        db.String(30),
        nullable=False
    )

    address_line_1 = db.Column(
        db.String(255),
        nullable=False
    )

    address_line_2 = db.Column(
        db.String(255),
        nullable=True
    )

    city = db.Column(
        db.String(100),
        nullable=False
    )

    state = db.Column(
        db.String(100),
        nullable=False
    )

    postal_code = db.Column(
        db.String(20),
        nullable=False
    )

    country = db.Column(
        db.String(100),
        nullable=False,
        default="India"
    )

    is_default = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )