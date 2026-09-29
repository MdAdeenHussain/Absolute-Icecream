from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db


user_roles = db.Table(
    "user_roles",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "role_id",
        db.Integer,
        db.ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Role(db.Model):
    """Application role."""

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(50),
        unique=True,
        nullable=False,
    )

    description = db.Column(db.String(255))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    users = db.relationship(
        "User",
        secondary=user_roles,
        back_populates="roles",
    )


class User(UserMixin, db.Model):
    """Application user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False,
    )

    first_name = db.Column(
        db.String(100),
        nullable=False,
    )

    last_name = db.Column(
        db.String(100),
    )

    phone = db.Column(
        db.String(30),
    )

    is_active = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
    )

    email_verified = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    marketing_consent = db.Column(
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

    roles = db.relationship(
        "Role",
        secondary=user_roles,
        back_populates="users",
    )

    addresses = db.relationship(
        "Address",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    orders = db.relationship(
        "Order",
        back_populates="user",
    )

    cart = db.relationship(
        "Cart",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    subscription = db.relationship(
        "Subscription",
        back_populates="user",
    )

    reward_account = db.relationship(
        "RewardAccount",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    reviews = db.relationship(
        "Review",
        back_populates="user",
    )

    audit_logs = db.relationship(
        "AuditLog",
        back_populates="user",
    )

    def set_password(self, password):
        """Hash and store a password."""

        self.password_hash = generate_password_hash(
            password
        )

    def check_password(self, password):
        """Check a plaintext password against the hash."""

        return check_password_hash(
            self.password_hash,
            password,
        )

    def has_role(self, role_name):
        """Return True if the user has the requested role."""

        return any(
            role.name == role_name
            for role in self.roles
        )

    @property
    def full_name(self):
        """Return the user's full name."""

        return " ".join(
            part
            for part in [
                self.first_name,
                self.last_name,
            ]
            if part
        )