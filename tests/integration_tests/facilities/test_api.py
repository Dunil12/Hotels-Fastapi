from first_project.src.schemas.facility import FacilityAdd


async def test_add_facility(ac):
    facility = FacilityAdd(title="title")
    new_facility = await ac.post("/facilities", json=facility.model_dump())

    assert new_facility.status_code == 200


async def test_get_all_facilities(ac):
    response = await ac.get("/facilities")

    assert response