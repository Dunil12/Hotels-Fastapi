

async def test_add_facility(ac):
    facility_title = "Массаж"
    response = await ac.post("/facilities", json={"title": facility_title})
    assert response.status_code == 200
    res = response.json()
    assert isinstance(res, dict)


async def test_get_all_facilities(ac):
    response = await ac.get("/facilities")

    assert response