from flask import Blueprint, abort, render_template

from app.models.product import Product


shop_bp = Blueprint(
    "shop",
    __name__,
    url_prefix=""
)


@shop_bp.route("/shop")
def shop():

    products = (
        Product.query
        .filter_by(is_active=True)
        .order_by(
            Product.is_featured.desc(),
            Product.created_at.desc()
        )
        .all()
    )

    return render_template(
        "shop.html",
        products=products
    )


@shop_bp.route("/shop/<slug>")
def product_detail(slug):

    product = (
        Product.query
        .filter_by(
            slug=slug,
            is_active=True
        )
        .first()
    )

    if not product:
        abort(404)

    variants = [
        variant
        for variant in product.variants
        if variant.is_active
    ]

    return render_template(
        "product.html",
        product=product,
        variants=variants
    )