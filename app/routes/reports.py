from flask import Blueprint, abort, render_template, send_file, url_for

from app.models.product import Product
from app.services.qr_service import generate_qr_code


reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


def _public_product(slug):
    product = Product.query.filter_by(slug=slug, is_active=True).first()
    if product is None:
        abort(404)
    return product


@reports_bp.get("/<slug>")
def product_report(slug):
    """Show the product-specific laboratory report and available facts."""
    product = _public_product(slug)
    return render_template("product_report.html", product=product)


@reports_bp.get("/qr/<slug>.png")
def product_report_qr(slug):
    """Generate a QR code that opens this product's report page."""
    _public_product(slug)
    report_url = url_for(
        "reports.product_report", slug=slug, _external=True
    )
    output = generate_qr_code(report_url)
    return send_file(output, mimetype="image/png", download_name=f"{slug}-report.png")
