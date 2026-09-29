from datetime import datetime

from app.extensions import db


class Coupon(db.Model):
    """Discount coupon."""

    __tablename__ = "coupons"

    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    description = db.Column(
        db.String(255),
    )

    discount_type = db.Column(
        db.String(30),
        nullable=False,
        default="percentage",
    )

    discount_value = db.Column(
        db.Numeric(10, 2),
        nullable=False,
    )

    minimum_order_value = db.Column(
        db.Numeric(10, 2),
        default=0,
        nullable=False,
    )

    maximum_discount = db.Column(
        db.Numeric(10, 2),
    )

    usage_limit = db.Column(
        db.Integer,
    )

    usage_count = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    starts_at = db.Column(
        db.DateTime,
    )

    expires_at = db.Column(
        db.DateTime,
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