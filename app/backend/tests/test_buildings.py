from pathlib import Path


FIXTURE_PATH = Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "minimal_ifc.xml"


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


def test_ifcxml_import_success(client):
    with FIXTURE_PATH.open("rb") as fixture:
        response = client.post(
            "/import/ifcxml",
            headers={"X-Role": "admin"},
            files={"file": ("minimal_ifc.xml", fixture, "application/xml")},
        )

    assert response.status_code == 201
    payload = response.json()
    assert payload["building_name"] == "HQ Building"
    assert payload["rooms_created"] == 2
    assert payload["walls_created"] == 2
    assert payload["windows_created"] == 1


def test_ifcxml_import_failure_has_reason(client):
    response = client.post(
        "/import/ifcxml",
        headers={"X-Role": "admin"},
        files={"file": ("broken.xml", b"<broken", "application/xml")},
    )

    assert response.status_code == 400
    assert "ifcXML import failed" in response.json()["detail"]


def test_monthly_co2_estimate_endpoint(client):
    with FIXTURE_PATH.open("rb") as fixture:
        imported = client.post(
            "/import/ifcxml",
            headers={"X-Role": "admin"},
            files={"file": ("minimal_ifc.xml", fixture, "application/xml")},
        )
    building_id = imported.json()["building_id"]

    response = client.get(f"/api/v1/co2/monthly?building_id={building_id}&working_days_per_month=20", headers={"X-Role": "viewer"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["building_id"] == building_id
    assert len(payload["rooms"]) == 2
    assert payload["total_monthly_kgco2"] > 0
