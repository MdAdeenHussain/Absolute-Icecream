from datetime import datetime

from app.extensions import db


class Review(db.Model):
    """Customer product review."""

    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False,
    )

    rating = db.Column(
        db.Integer,
        nullable=False,
    )

    title = db.Column(
        db.String(150),
    )

    body = db.Column(
        db.Text,
    )

    is_verified_purchase = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    moderation_status = db.Column(
        db.String(30),
        nullable=False,
        default="pending",
    )

    is_featured = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user = db.relationship(
        "User",
        back_populates="reviews",
    )

    product = db.relationship(
        "Product",
        back_populates="reviews",
    )