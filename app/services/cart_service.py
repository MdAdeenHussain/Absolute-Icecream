from decimal import Decimal

from app.models.product import ProductVariant


class CartService:

    SESSION_KEY = "absolute_cart"

    @classmethod
    def get_cart(cls, session):
        return session.get(cls.SESSION_KEY, {})

    @classmethod
    def save_cart(cls, session, cart):
        session[cls.SESSION_KEY] = cart
        session.modified = True

    @classmethod
    def add(
        cls,
        session,
        variant_id,
        quantity=1
    ):
        cart = cls.get_cart(session)

        variant_key = str(variant_id)

        current_quantity = cart.get(
            variant_key,
            0
        )

        cart[variant_key] = (
            current_quantity + quantity
        )

        cls.save_cart(session, cart)

        return cart

    @classmethod
    def update(
        cls,
        session,
        variant_id,
        quantity
    ):
        cart = cls.get_cart(session)

        variant_key = str(variant_id)

        if quantity <= 0:
            cart.pop(variant_key, None)
        else:
            cart[variant_key] = quantity

        cls.save_cart(session, cart)

        return cart

    @classmethod
    def remove(
        cls,
        session,
        variant_id
    ):
        cart = cls.get_cart(session)

        cart.pop(str(variant_id), None)

        cls.save_cart(session, cart)

        return cart

    @classmethod
    def clear(cls, session):
        session.pop(cls.SESSION_KEY, None)

    @classmethod
    def hydrate(cls, session):

        cart = cls.get_cart(session)

        if not cart:
            return {
                "items": [],
                "subtotal": Decimal("0.00"),
                "item_count": 0
            }

        variant_ids = []

        for variant_id in cart:
            try:
                variant_ids.append(int(variant_id))
            except ValueError:
                continue

        variants = (
            ProductVariant.query
            .filter(
                ProductVariant.id.in_(variant_ids)
            )
            .all()
        )

        variant_map = {
            str(variant.id): variant
            for variant in variants
        }

        items = []

        subtotal = Decimal("0.00")
        item_count = 0

        for variant_id, quantity in cart.items():

            variant = variant_map.get(
                str(variant_id)
            )

            if not variant:
                continue

            quantity = int(quantity)

            line_total = (
                variant.price * quantity
            )

            subtotal += line_total
            item_count += quantity

            items.append({
                "variant_id": variant.id,
                "product_id": variant.product_id,
                "name": variant.product.name,
                "flavour": variant.product.flavour,
                "size": variant.size,
                "volume_ml": variant.volume_ml,
                "price": float(variant.price),
                "quantity": quantity,
                "line_total": float(line_total),
                "image": variant.product.image,
                "stock": variant.stock_quantity,
            })

        return {
            "items": items,
            "subtotal": float(subtotal),
            "item_count": item_count
        }