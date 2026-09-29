"""Application factory for Absolute Icecream."""

import os

from flask import Flask, render_template

from app.config import config_by_name
from app.extensions import db, login_manager, migrate


def create_app(config_name=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    config_name = config_name or os.getenv("FLASK_CONFIG") or os.getenv(
        "FLASK_ENV", "development"
    )
    try:
        config = config_by_name[config_name]
    except KeyError as exc:
        raise ValueError(f"Unknown Flask configuration: {config_name}") from exc

    app.config.from_object(config)
    if config_name == "production" and not os.getenv("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY must be configured in production.")

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import every model before Flask-Migrate inspects db.metadata.
    from app import models as _models  # noqa: F401
    from app.models.customer import Customer

    @app.context_processor
    def inject_customer_context():
        from app.utils.auth import current_customer
        return {
            "brand_name": "Absolute Icecream™",
            "brand_tagline": "Real taste. No compromises.",
            "current_customer": current_customer(),
            "current_year": 2026,
        }

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Customer, int(user_id))

    from app.routes.account import account_bp
    from app.routes.admin import admin_bp
    from app.routes.auth import auth_bp
    from app.routes.cart import cart_bp
    from app.routes.checkout import checkout_bp
    from app.routes.main import main_bp
    from app.routes.shop import shop_bp
    from app.routes.reports import reports_bp

    for blueprint in (main_bp, shop_bp, cart_bp, checkout_bp, reports_bp, auth_bp,
                      account_bp, admin_bp):
        app.register_blueprint(blueprint)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    return app
