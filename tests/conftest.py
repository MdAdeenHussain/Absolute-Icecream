import pytest

from app import create_app
from app.extensions import db
from app.models import Admin, Flavor, Product, ProductVariant


@pytest.fixture()
def app(monkeypatch):
    monkeypatch.setenv("TEST_DATABASE_URL", "sqlite://")
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        flavor = Flavor(name="Vanilla", slug="vanilla")
        product = Product(
            name="Vanilla", slug="vanilla", sku="VAN-001", flavor=flavor,
            launch_status="launch", product_status="live", is_active=True,
            nutrition_status="pending",
        )
        variant = ProductVariant(
            product=product, name="100 ml", sku="VAN-001-100", size_ml=100,
            mrp=120, selling_price=110, inventory_quantity=10, is_available=True,
        )
        admin = Admin(name="Admin", email="admin@example.com", role="admin")
        admin.set_password("Admin123!")
        db.session.add_all([flavor, product, variant, admin])
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()
