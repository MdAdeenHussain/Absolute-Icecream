from datetime import datetime

from app.extensions import db


class BlogPost(db.Model):
    """Journal/blog article."""

    __tablename__ = "blog_posts"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(255),
        nullable=False,
    )

    slug = db.Column(
        db.String(300),
        unique=True,
        nullable=False,
    )

    excerpt = db.Column(
        db.Text,
    )

    content = db.Column(
        db.Text,
    )

    cover_image = db.Column(
        db.String(500),
    )

    category = db.Column(
        db.String(80),
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="draft",
    )

    published_at = db.Column(
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


class NewsletterSubscriber(db.Model):
    """Newsletter subscriber."""

    __tablename__ = "newsletter_subscribers"

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    is_confirmed = db.Column(
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


class ContactMessage(db.Model):
    """Customer contact form submission."""

    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(150),
        nullable=False,
    )

    email = db.Column(
        db.String(255),
        nullable=False,
    )

    subject = db.Column(
        db.String(255),
    )

    message = db.Column(
        db.Text,
        nullable=False,
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="new",
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )