from fastapi import APIRouter

from fastapi_cache.decorator import cache

from first_project.src.api.dependencies import DBDep
from first_project.src.schemas.facility import Facility, FacilityAdd
from first_project.src.tasks.tasks import test_task
# from ..tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получение полного вписка удобств")
@cache(expire=10)
async def get_all_facilities(
        db: DBDep,
) -> list[Facility] | None:
    return await db.facilities.get_all()


@router.post("}", summary="Создание записи в БД удобства(facilities)")
async def add_facility(
        db: DBDep,
        facility_data: FacilityAdd
):
    await db.facilities.add(facility_data)
    await db.commit()

    test_task.delay()

    return {"status": "OK"}