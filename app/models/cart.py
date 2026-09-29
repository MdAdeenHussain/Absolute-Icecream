from datetime import datetime

from app.extensions import db


class Cart(db.Model):
    """Shopping cart belonging to a user."""

    __tablename__ = "carts"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
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
        back_populates="cart",
    )

    items = db.relationship(
        "CartItem",
        back_populates="cart",
        cascade="all, delete-orphan",
    )


class CartItem(db.Model):
    """Individual cart item."""

    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)

    cart_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "carts.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    variant_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "product_variants.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    quantity = db.Column(
        db.Integer,
        nullable=False,
        default=1,
    )

    is_subscription = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    cart = db.relationship(
        "Cart",
        back_populates="items",
    )

    variant = db.relationship(
        "ProductVariant",
        back_populates="cart_items",
    )

    __table_args__ = (
        db.UniqueConstraint(
            "cart_id",
            "variant_id",
            name="uq_cart_variant",
        ),
    )