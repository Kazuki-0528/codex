def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_building_crud_with_permission_checks(client):
    create_payload = {"name": "HQ", "location": "Tokyo", "gross_area_m2": 1000}

    denied = client.post("/api/v1/buildings", json=create_payload, headers={"X-Role": "viewer"})
    assert denied.status_code == 403

    created = client.post("/api/v1/buildings", json=create_payload, headers={"X-Role": "admin"})
    assert created.status_code == 201
    building_id = created.json()["id"]

    listed = client.get("/api/v1/buildings", headers={"X-Role": "viewer"})
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    updated = client.patch(
        f"/api/v1/buildings/{building_id}",
        json={"location": "Osaka"},
        headers={"X-Role": "fm_manager"},
    )
    assert updated.status_code == 200
    assert updated.json()["location"] == "Osaka"


def test_validation_error(client):
    response = client.post(
        "/api/v1/buildings",
        json={"name": "A", "location": "B", "gross_area_m2": 0},
        headers={"X-Role": "admin"},
    )
    assert response.status_code == 422
