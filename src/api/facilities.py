from fastapi import APIRouter

from first_project.src.api.dependencies import DBDep
from first_project.src.schemas.facility import Facility, FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("", summary="Получение полного вписка удобств")
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

    return {"status": "OK"}