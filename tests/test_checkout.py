def test_checkout_recalculates_cart_and_creates_pending_order(client):
    client.post("/api/cart/add", json={"variant_id": 1, "quantity": 2})
    response = client.post("/api/checkout/create", json={
        "name": "Guest", "email": "guest@example.com", "phone": "9999999999",
        "address_line_1": "1 Test Street", "city": "Mumbai", "state": "MH",
        "postal_code": "400001",
    })
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["payment_required"] is True
    assert payload["total"] == 220.0
    assert client.get(f"/checkout/payment/{payload['order_id']}").status_code == 200
