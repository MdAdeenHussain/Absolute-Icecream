import sys

from app import create_app
from app.extensions import db
from app.models import (
    Flavor,
    Ingredient,
    Product,
    ProductClaim,
    ProductImage,
    ProductIngredient,
    ProductVariant,
)


FLAVORS = [
    {
        "name": "Dark Chocolate",
        "slug": "dark-chocolate",
        "description": (
            "A deep chocolate-forward flavor "
            "designed for a rich, indulgent profile."
        ),
        "accent_color": "#315E68",
        "launch_status": "launch",
    },
    {
        "name": "Classic Vanilla",
        "slug": "classic-vanilla",
        "description": (
            "A classic vanilla profile with a "
            "clean, premium presentation."
        ),
        "accent_color": "#E8D5A8",
        "launch_status": "launch",
    },
    {
        "name": "Strawberry",
        "slug": "strawberry",
        "description": (
            "A strawberry concept using the supplied "
            "brand photography."
        ),
        "accent_color": "#E96A7A",
        "launch_status": "coming_soon",
    },
    {
        "name": "Alphonso Mango",
        "slug": "alphonso-mango",
        "description": (
            "An Alphonso mango concept using the supplied "
            "brand photography."
        ),
        "accent_color": "#F5A623",
        "launch_status": "coming_soon",
    },
    {
        "name": "Cookies & Cream",
        "slug": "cookies-and-cream",
        "description": (
            "A cookies and cream concept using the supplied "
            "brand photography."
        ),
        "accent_color": "#315E68",
        "launch_status": "coming_soon",
    },
]


INGREDIENTS = [
    {
        "name": "Low-Lactose Dairy Base",
        "slug": "low-lactose-dairy-base",
        "category": "Dairy Base",
        "description": (
            "Proposed dairy base with lactose reduction "
            "through filtration, subject to formulation "
            "and testing."
        ),
    },
    {
        "name": "Cream",
        "slug": "cream",
        "category": "Dairy",
        "description": (
            "Cream included as part of the proposed "
            "dairy formulation."
        ),
    },
    {
        "name": "Milk Protein",
        "slug": "milk-protein",
        "category": "Protein",
        "description": (
            "Milk protein included in the proposed "
            "formulation."
        ),
    },
    {
        "name": "Monk Fruit / Stevia",
        "slug": "monk-fruit-stevia",
        "category": "Sweetener",
        "description": (
            "Proposed sweetener system. Final selection "
            "and regulatory classification remain subject "
            "to formulation and review."
        ),
    },
    {
        "name": "Zero-Sugar Bulking System",
        "slug": "zero-sugar-bulking-system",
        "category": "Formulation",
        "description": (
            "Proposed bulking approach for formulation "
            "development."
        ),
    },
]


PRODUCTS = [
    {
        "name": "Dark Chocolate",
        "slug": "dark-chocolate",
        "sku": "ABS-DCH-001",
        "flavor": "dark-chocolate",
        "launch_status": "launch",
        "product_status": "draft",
        "short_description": (
            "Rich chocolate profile with a deep cocoa character."
        ),
        "image": (
            "images/products/dark-chocolate.JPG"
        ),
    },
    {
        "name": "Classic Vanilla",
        "slug": "classic-vanilla",
        "sku": "ABS-VAN-001",
        "flavor": "classic-vanilla",
        "launch_status": "launch",
        "product_status": "draft",
        "short_description": (
            "A classic vanilla profile with a premium finish."
        ),
        "image": (
            "images/products/vanilla.JPG"
        ),
    },
    {
        "name": "Strawberry",
        "slug": "strawberry",
        "sku": "ABS-STR-001",
        "flavor": "strawberry",
        "launch_status": "coming_soon",
        "product_status": "draft",
        "short_description": (
            "Strawberry concept shown in supplied photography."
        ),
        "image": (
            "images/products/strawberry.JPG"
        ),
    },
    {
        "name": "Alphonso Mango",
        "slug": "alphonso-mango",
        "sku": "ABS-MNG-001",
        "flavor": "alphonso-mango",
        "launch_status": "coming_soon",
        "product_status": "draft",
        "short_description": (
            "Alphonso mango concept shown in supplied photography."
        ),
        "image": (
            "images/products/mango.JPG"
        ),
    },
    {
        "name": "Cookies & Cream",
        "slug": "cookies-and-cream",
        "sku": "ABS-CNC-001",
        "flavor": "cookies-and-cream",
        "launch_status": "coming_soon",
        "product_status": "draft",
        "short_description": (
            "Cookies and cream concept shown in supplied photography."
        ),
        "image": (
            "images/products/cookie-n-cream.JPG"
        ),
    },
]


def seed_products():
    """Seed flavors, ingredients and products."""

    app = create_app("development")

    with app.app_context():

        for flavor_data in FLAVORS:

            flavor = Flavor.query.filter_by(
                slug=flavor_data["slug"]
            ).first()

            if flavor is None:
                flavor = Flavor(**flavor_data)
                db.session.add(flavor)

        for ingredient_data in INGREDIENTS:

            ingredient = Ingredient.query.filter_by(
                slug=ingredient_data["slug"]
            ).first()

            if ingredient is None:
                ingredient = Ingredient(
                    **ingredient_data
                )
                db.session.add(ingredient)

        db.session.commit()

        for product_data in PRODUCTS:

            existing = Product.query.filter_by(
                slug=product_data["slug"]
            ).first()

            if existing:
                continue

            flavor = Flavor.query.filter_by(
                slug=product_data["flavor"]
            ).first()

            product = Product(
                name=product_data["name"],
                slug=product_data["slug"],
                sku=product_data["sku"],
                flavor=flavor,
                launch_status=product_data[
                    "launch_status"
                ],
                product_status=product_data[
                    "product_status"
                ],
                short_description=product_data[
                    "short_description"
                ],
                nutrition_status="to_be_finalized",
            )

            db.session.add(product)
            db.session.flush()

            image = ProductImage(
                product=product,
                image_path=product_data["image"],
                alt_text=(
                    f"{product.name} Absolute Icecream "
                    "product photography"
                ),
                image_type="product",
                is_primary=True,
                display_order=0,
            )

            db.session.add(image)

            variant_100 = ProductVariant(
                product=product,
                name="100 ml",
                sku=f"{product_data['sku']}-100",
                size_ml=100,
                weight_grams=100,
                mrp=120,
                selling_price=120,
                inventory_quantity=20,
                is_available=True,
            )

            variant_500 = ProductVariant(
                product=product,
                name="500 ml",
                sku=f"{product_data['sku']}-500",
                size_ml=500,
                weight_grams=500,
                mrp=450,
                selling_price=450,
                inventory_quantity=20,
                is_available=True,
            )

            db.session.add_all([
                variant_100,
                variant_500,
            ])

            target_claim = ProductClaim(
                product=product,
                claim_text=(
                    "≤0.5g total sugars / 100g"
                ),
                claim_type="product_target",
                status="target",
                regulatory_reviewed=False,
                is_public=False,
            )

            db.session.add(target_claim)

        db.session.commit()

        print(
            "Absolute Icecream product seed completed."
        )


if __name__ == "__main__":
    try:
        seed_products()
    except Exception as exc:
        print(
            f"Product seed failed: {exc}",
            file=sys.stderr,
        )
        raise
