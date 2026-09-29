from datetime import datetime

from app.extensions import db


class Address(db.Model):
    """Customer shipping/billing address."""

    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    label = db.Column(
        db.String(50),
        default="Home",
    )

    recipient_name = db.Column(
        db.String(200),
        nullable=False,
    )

    phone = db.Column(
        db.String(30),
        nullable=False,
    )

    address_line_1 = db.Column(
        db.String(255),
        nullable=False,
    )

    address_line_2 = db.Column(
        db.String(255),
    )

    city = db.Column(
        db.String(100),
        nullable=False,
    )

    state = db.Column(
        db.String(100),
        nullable=False,
    )

    postal_code = db.Column(
        db.String(20),
        nullable=False,
    )

    country = db.Column(
        db.String(100),
        nullable=False,
        default="India",
    )

    is_default = db.Column(
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
        back_populates="addresses",
    )

    orders = db.relationship(
        "Order",
        back_populates="shipping_address",
    )


class Order(db.Model):
    """Customer order."""

    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    order_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=True,
    )

    shipping_address_id = db.Column(
        db.Integer,
        db.ForeignKey("addresses.id"),
    )

    status = db.Column(
        db.String(40),
        nullable=False,
        default="pending",
    )

    payment_status = db.Column(
        db.String(40),
        nullable=False,
        default="pending",
    )

    payment_provider = db.Column(
        db.String(50),
    )

    payment_reference = db.Column(
        db.String(255),
    )

    currency = db.Column(
        db.String(10),
        default="INR",
        nullable=False,
    )

    subtotal = db.Column(
        db.Numeric(12, 2),
        nullable=False,
        default=0,
    )

    discount_amount = db.Column(
        db.Numeric(12, 2),
        nullable=False,
        default=0,
    )

    shipping_amount = db.Column(
        db.Numeric(12, 2),
        nullable=False,
        default=0,
    )

    tax_amount = db.Column(
        db.Numeric(12, 2),
        nullable=False,
        default=0,
    )

    total_amount = db.Column(
        db.Numeric(12, 2),
        nullable=False,
        default=0,
    )

    coupon_code = db.Column(
        db.String(100),
    )

    notes = db.Column(
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

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("customers.id"),
        nullable=True,
        index=True
    )
    
    user = db.relationship(
        "User",
        back_populates="orders",
    )

    customer = db.relationship(
        "Customer",
        back_populates="orders",
    )

    shipping_address = db.relationship(
        "Address",
        back_populates="orders",
    )

    items = db.relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )

    @property
    def total(self):
        return self.total_amount

    @property
    def shipping_fee(self):
        return self.shipping_amount

    @property
    def discount(self):
        return self.discount_amount

    @property
    def customer_email(self):
        return self.customer.email if self.customer else "Guest checkout"


class OrderItem(db.Model):
    """Individual item in an order."""

    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "orders.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("products.id"),
        nullable=False,
    )

    variant_id = db.Column(
        db.Integer,
        db.ForeignKey("product_variants.id"),
        nullable=False,
    )

    product_name = db.Column(
        db.String(150),
        nullable=False,
    )

    variant_name = db.Column(
        db.String(100),
        nullable=False,
    )

    quantity = db.Column(
        db.Integer,
        nullable=False,
    )

    unit_price = db.Column(
        db.Numeric(10, 2),
        nullable=False,
    )

    total_price = db.Column(
        db.Numeric(12, 2),
        nullable=False,
    )

    order = db.relationship(
        "Order",
        back_populates="items",
    )

    product = db.relationship(
        "Product",
        back_populates="order_items",
    )

    variant = db.relationship(
        "ProductVariant",
        back_populates="order_items",
    )

    @property
    def variant_size(self):
        return self.variant_name

    @property
    def line_total(self):
        return self.total_price
