from datetime import datetime

from app.extensions import db


class RewardAccount(db.Model):
    """Customer rewards account."""

    __tablename__ = "reward_accounts"

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

    points_balance = db.Column(
        db.Integer,
        nullable=False,
        default=0,
    )

    lifetime_points = db.Column(
        db.Integer,
        nullable=False,
        default=0,
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
        back_populates="reward_account",
    )

    transactions = db.relationship(
        "RewardTransaction",
        back_populates="account",
        cascade="all, delete-orphan",
    )


class RewardTransaction(db.Model):
    """Reward points transaction."""

    __tablename__ = "reward_transactions"

    id = db.Column(db.Integer, primary_key=True)

    account_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "reward_accounts.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    points = db.Column(
        db.Integer,
        nullable=False,
    )

    transaction_type = db.Column(
        db.String(50),
        nullable=False,
    )

    description = db.Column(
        db.String(255),
    )

    reference_type = db.Column(
        db.String(50),
    )

    reference_id = db.Column(
        db.String(100),
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    account = db.relationship(
        "RewardAccount",
        back_populates="transactions",
    )