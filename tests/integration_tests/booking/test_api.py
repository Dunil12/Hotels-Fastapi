import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize(
    "booking_data, expected_status_code",
    [
        # Успешное создание бронирования
        (
            {
                "date_from": "2025-08-08",
                "date_to": "2025-08-15",
                "room_id": 1  # Динамически получаем room_id
            },
            200,
        ),
        # Некорректные даты (date_from позже date_to)
        (
            {
                "date_from": "2025-08-02",
                "date_to": "2025-08-01",
                "room_id": 1
            },
            400,
        ),
        # Несуществующий room_id
        (
            {
                "date_from": "2025-08-08",
                "date_to": "2025-08-15",
                "room_id": 999999  # Предполагаем, что такого ID нет
            },
            404,
        ),
        # Случай, вызывающий ошибку валидации данных
        (
            {
                "date_from": "invalid-date",  # Некорректный формат даты
                "date_to": "2025-08-02",
                "room_id": 1
            },
            422,  # Unprocessable Entity
        ),
    ],
    ids=["success", "invalid_dates", "invalid_room_id", "validation_error"]
)
async def test_create_booking(db, authenticated_ac, booking_data, expected_status_code):

    payload = {
        "date_from": booking_data["date_from"],
        "date_to": booking_data["date_to"],
        "room_id": booking_data["room_id"]
    }

    response = await authenticated_ac.post(url="/bookings", json=payload)

    assert response.status_code == expected_status_code, (
        f"Expected status code {expected_status_code}, but got {response.status_code}. "
        f"Response: {response.text}"
    )

    if response.status_code == 200:
        booking = response.json()
        assert isinstance(booking, dict)
        assert booking["data"]


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for db_ in get_db_null_pool():
        await db_.bookings.delete()
        await db_.commit()

@pytest.mark.parametrize("date_from, date_to, room_id, expected_bookings_count",
[
    ("2025-08-01", "2025-08-05", 1, 1),
    ("2025-08-01", "2025-08-05", 1, 2),
    ("2025-08-01", "2025-08-05", 1, 3),
])
async def test_get_my_bookings(date_from, date_to, room_id, expected_bookings_count, authenticated_ac, delete_all_bookings,):
    payload = {
        "date_from": date_from,
        "date_to": date_to,
        "room_id": room_id
    }

    await authenticated_ac.post(url="/bookings", json=payload)
    response = await authenticated_ac.get("/bookings/me")

    assert response.status_code == 200

    bookings = response.json()
    assert isinstance(bookings, list)
    assert len(bookings) == expected_bookings_count