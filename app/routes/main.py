from flask import Blueprint, abort, render_template

main_bp = Blueprint(
    "main",
    __name__,
)


@main_bp.get("/")
def index():
    """Render the Absolute Icecream homepage."""

    return render_template(
        "home.html"
    )


@main_bp.get("/pages/<page>")
@main_bp.get("/<page>")
def information_page(page):
    """Serve the informational pages linked from the public navigation."""
    pages = {
        "why-absolute": ("Why Absolute", "A better ice cream experience starts with clarity."),
        "our-story": ("Our Story", "Absolute Icecream is built around real taste and transparent information."),
        "ingredients": ("Ingredients", "Ingredient details are published as each formulation is finalised."),
        "journal": ("Journal", "Stories, product notes, and updates from Absolute Icecream."),
        "subscribe": ("Subscriptions", "Subscription availability will be announced before launch."),
        "rewards": ("Rewards", "Rewards will become available when the programme launches."),
        "contact": ("Contact", "For product and order enquiries, contact the Absolute Icecream team."),
        "shipping": ("Shipping", "Shipping availability and delivery windows are shown at checkout."),
        "refunds": ("Refunds", "Refund guidance will be published before orders open."),
        "privacy": ("Privacy", "We use customer information only to operate and improve the service."),
        "terms": ("Terms", "Terms of sale and use will be published before launch."),
        "cookies": ("Cookies", "Cookie preferences are managed in your browser."),
    }
    content = pages.get(page)
    if content is None:
        abort(404)
    return render_template("information.html", title=content[0], body=content[1])
