def test_admin_login_and_dashboard_authorization(client):
    assert client.get("/admin/").status_code == 302
    response = client.post("/admin/login", data={
        "email": "admin@example.com", "password": "Admin123!",
    }, follow_redirects=True)
    assert response.status_code == 200
    assert client.get("/admin/products").status_code == 200
    assert client.get("/admin/batches").status_code == 404
