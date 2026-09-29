from app.models.customer import Customer


def normalize_email(email):
    return (email or "").strip().lower()


def authenticate_customer(email, password):
    email = normalize_email(email)

    customer = Customer.query.filter_by(
        email=email
    ).first()

    if not customer:
        return None

    if not customer.is_active:
        return None

    if not customer.check_password(password):
        return None

    return customer