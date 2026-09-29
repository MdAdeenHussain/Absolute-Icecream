def test_customer_register_login_and_account_access(client):
    response = client.post("/account/register", data={
        "first_name": "Jane", "email": "jane@example.com", "password": "Password1!",
        "confirm_password": "Password1!",
    })
    assert response.status_code == 302
    assert client.get("/account/").status_code == 200
    assert client.get("/account/orders").status_code == 200
    assert client.get("/account/logout").status_code == 302
    assert client.get("/account/").status_code == 302
