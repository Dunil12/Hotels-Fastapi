from first_project.tests.conftest import ac

async def test_get_all_hotels(ac, setup_database, fill_database):
    response = await ac.get("/hotels", params={
        "page": 1,
        "per_page": 5,
        "date_from": "2025-05-10",
        "date_to": "2025-05-11"
    })

    assert response.status_code == 200