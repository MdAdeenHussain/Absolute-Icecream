from datetime import datetime

from app.extensions import db


class AuditLog(db.Model):
    """Administrative activity log."""

    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
    )

    action = db.Column(
        db.String(100),
        nullable=False,
    )

    entity_type = db.Column(
        db.String(100),
    )

    entity_id = db.Column(
        db.String(100),
    )

    old_value = db.Column(
        db.Text,
    )

    new_value = db.Column(
        db.Text,
    )

    ip_address = db.Column(
        db.String(64),
    )

    user_agent = db.Column(
        db.Text,
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    user = db.relationship(
        "User",
        back_populates="audit_logs",
    )