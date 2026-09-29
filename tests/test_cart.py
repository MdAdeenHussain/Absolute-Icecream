def test_cart_add_update_and_remove(client):
    assert client.get("/api/cart").get_json()["item_count"] == 0
    response = client.post("/api/cart/add", json={"variant_id": 1, "quantity": 2})
    assert response.status_code == 200
    assert response.get_json()["item_count"] == 2
    response = client.patch("/api/cart/update", json={"variant_id": 1, "quantity": 3})
    assert response.get_json()["item_count"] == 3
    assert client.delete("/api/cart/remove/1").get_json()["item_count"] == 0
