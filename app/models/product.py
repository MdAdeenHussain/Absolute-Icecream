from datetime import datetime

from app.extensions import db


class Product(db.Model):
    """Ice cream product."""

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(150),
        nullable=False,
    )

    slug = db.Column(
        db.String(180),
        unique=True,
        nullable=False,
        index=True,
    )

    sku = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
    )

    short_description = db.Column(
        db.String(500),
    )

    description = db.Column(
        db.Text,
    )

    flavor_id = db.Column(
        db.Integer,
        db.ForeignKey("flavors.id"),
        nullable=False,
    )

    launch_status = db.Column(
        db.String(30),
        nullable=False,
        default="coming_soon",
    )

    product_status = db.Column(
        db.String(30),
        nullable=False,
        default="draft",
    )

    is_featured = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
    )

    ingredients_text = db.Column(
        db.Text,
    )

    nutrition_status = db.Column(
        db.String(40),
        nullable=False,
        default="to_be_finalized",
    )

    allergen_information = db.Column(
        db.Text,
    )

    storage_instructions = db.Column(
        db.Text,
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

    flavor = db.relationship(
        "Flavor",
        back_populates="products",
    )

    variants = db.relationship(
        "ProductVariant",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    images = db.relationship(
        "ProductImage",
        back_populates="product",
        cascade="all, delete-orphan",
        order_by="ProductImage.display_order",
    )

    ingredient_links = db.relationship(
        "ProductIngredient",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    claims = db.relationship(
        "ProductClaim",
        back_populates="product",
        cascade="all, delete-orphan",
    )

    order_items = db.relationship(
        "OrderItem",
        back_populates="product",
    )

    reviews = db.relationship(
        "Review",
        back_populates="product",
    )

    @property
    def primary_image(self):
        """Return the first primary product image."""

        for image in self.images:
            if image.is_primary:
                return image

        return self.images[0] if self.images else None

    @property
    def flavour(self):
        return self.flavor.name if self.flavor else ""

    @property
    def image(self):
        image = self.primary_image
        return image.image_path if image else None


class ProductVariant(db.Model):
    """Sellable product format."""

    __tablename__ = "product_variants"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "products.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    name = db.Column(
        db.String(100),
        nullable=False,
    )

    sku = db.Column(
        db.String(80),
        unique=True,
        nullable=False,
    )

    size_ml = db.Column(
        db.Integer,
        nullable=False,
    )

    weight_grams = db.Column(
        db.Numeric(10, 2),
    )

    mrp = db.Column(
        db.Numeric(10, 2),
        nullable=False,
    )

    selling_price = db.Column(
        db.Numeric(10, 2),
        nullable=False,
    )

    inventory_quantity = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    low_stock_threshold = db.Column(
        db.Integer,
        default=10,
        nullable=False,
    )

    is_available = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    product = db.relationship(
        "Product",
        back_populates="variants",
    )

    order_items = db.relationship(
        "OrderItem",
        back_populates="variant",
    )

    cart_items = db.relationship(
        "CartItem",
        back_populates="variant",
    )

    @property
    def price(self):
        return self.selling_price

    @property
    def size(self):
        return self.name

    @property
    def volume_ml(self):
        return self.size_ml

    @property
    def stock_quantity(self):
        return self.inventory_quantity

    @property
    def is_active(self):
        return self.is_available


class ProductImage(db.Model):
    """Product image metadata."""

    __tablename__ = "product_images"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "products.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    image_path = db.Column(
        db.String(500),
        nullable=False,
    )

    alt_text = db.Column(
        db.String(255),
    )

    image_type = db.Column(
        db.String(40),
        default="product",
        nullable=False,
    )

    display_order = db.Column(
        db.Integer,
        default=0,
        nullable=False,
    )

    is_primary = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    product = db.relationship(
        "Product",
        back_populates="images",
    )


class ProductClaim(db.Model):
    """
    Configurable product/marketing claim.

    A claim should only be displayed as verified when
    its status has been explicitly changed by an
    authorized administrator.
    """

    __tablename__ = "product_claims"

    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "products.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    claim_text = db.Column(
        db.String(500),
        nullable=False,
    )

    claim_type = db.Column(
        db.String(50),
        nullable=False,
        default="product_target",
    )

    status = db.Column(
        db.String(40),
        nullable=False,
        default="draft",
    )

    evidence_reference = db.Column(
        db.String(500),
    )

    verification_date = db.Column(
        db.DateTime,
    )

    regulatory_reviewed = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    is_public = db.Column(
        db.Boolean,
        default=False,
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

    product = db.relationship(
        "Product",
        back_populates="claims",
    )
