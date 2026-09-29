def test_storefront_and_product_detail_render(client):
    assert client.get("/").status_code == 200
    assert client.get("/shop").status_code == 200
    assert client.get("/shop/vanilla").status_code == 200
