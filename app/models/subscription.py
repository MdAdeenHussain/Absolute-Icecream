from datetime import datetime

from app.extensions import db


class Subscription(db.Model):
    """Recurring ice cream subscription."""

    __tablename__ = "subscriptions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    provider_subscription_id = db.Column(
        db.String(255),
    )

    status = db.Column(
        db.String(40),
        nullable=False,
        default="pending",
    )

    frequency = db.Column(
        db.String(30),
        nullable=False,
        default="every_4_weeks",
    )

    next_billing_date = db.Column(
        db.Date,
    )

    paused_until = db.Column(
        db.Date,
    )

    cancelled_at = db.Column(
        db.DateTime,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    user = db.relationship(
        "User",
        back_populates="subscription",
    )

    items = db.relationship(
        "SubscriptionItem",
        back_populates="subscription",
        cascade="all, delete-orphan",
    )


class SubscriptionItem(db.Model):
    """Product included in a subscription."""

    __tablename__ = "subscription_items"

    id = db.Column(db.Integer, primary_key=True)

    subscription_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "subscriptions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    variant_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "product_variants.id",
        ),
        nullable=False,
    )

    quantity = db.Column(
        db.Integer,
        nullable=False,
        default=1,
    )

    subscription = db.relationship(
        "Subscription",
        back_populates="items",
    )

    variant = db.relationship(
        "ProductVariant",
    )