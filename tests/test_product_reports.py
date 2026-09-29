def test_product_report_page_and_qr(client):
    detail = client.get("/shop/vanilla")
    assert detail.status_code == 200
    assert b"Product lab report" in detail.data
    assert b"/reports/vanilla" in detail.data
    assert b"/reports/qr/vanilla.png" in detail.data

    report = client.get("/reports/vanilla")
    assert report.status_code == 200
    assert b"Vanilla" in report.data
    assert b"Results not yet published" in report.data
    assert b"0.38" not in report.data

    qr = client.get("/reports/qr/vanilla.png")
    assert qr.status_code == 200
    assert qr.mimetype == "image/png"


def test_reports_are_available_for_each_active_product(client, app):
    from app.extensions import db
    from app.models import Flavor, Product

    with app.app_context():
        flavor = Flavor.query.filter_by(slug="chocolate").first()
        if flavor is None:
            flavor = Flavor(name="Chocolate", slug="chocolate")
            db.session.add(flavor)
            db.session.flush()
        product = Product(
            name="Dark Chocolate",
            slug="dark-chocolate",
            sku="DCH-001",
            flavor=flavor,
            is_active=True,
        )
        db.session.add(product)
        db.session.commit()

    assert client.get("/reports/dark-chocolate").status_code == 200
    assert client.get("/reports/qr/dark-chocolate.png").status_code == 200
    assert client.get("/reports/unknown-product").status_code == 404
    assert client.get("/verify/van-001").status_code == 404