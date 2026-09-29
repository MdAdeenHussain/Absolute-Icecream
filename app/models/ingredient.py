from datetime import datetime

from app.extensions import db


class Ingredient(db.Model):
    """Ingredient used in one or more products."""

    __tablename__ = "ingredients"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(150),
        unique=True,
        nullable=False,
    )

    slug = db.Column(
        db.String(180),
        unique=True,
        nullable=False,
    )

    description = db.Column(
        db.Text,
    )

    category = db.Column(
        db.String(80),
    )

    is_public = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    product_links = db.relationship(
        "ProductIngredient",
        back_populates="ingredient",
        cascade="all, delete-orphan",
    )


class ProductIngredient(db.Model):
    """Association between a product and ingredient."""

    __tablename__ = "product_ingredients"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "products.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    ingredient_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "ingredients.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    display_order = db.Column(
        db.Integer,
        default=0,
        nullable=False,
    )

    notes = db.Column(
        db.Text,
    )

    product = db.relationship(
        "Product",
        back_populates="ingredient_links",
    )

    ingredient = db.relationship(
        "Ingredient",
        back_populates="product_links",
    )

    __table_args__ = (
        db.UniqueConstraint(
            "product_id",
            "ingredient_id",
            name="uq_product_ingredient",
        ),
    )