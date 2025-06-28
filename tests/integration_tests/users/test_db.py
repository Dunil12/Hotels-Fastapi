from first_project.src.database import async_session_maker, async_session_maker_null_pool
from first_project.src.schemas.users import UserRequestAdd, UserAdd
from first_project.src.services.auth import AuthService
from first_project.src.utils.db_manager import DBManager


# async def test_register_user():
#     user_data = UserRequestAdd(email="email@gmail.com", password="password")
#     hashed_password = AuthService().hash_password(user_data.password)
#     new_user_data = UserAdd(email=user_data.email, hashed_password=hashed_password)
#
#     async with DBManager(session_factory=async_session_maker_null_pool) as db:
#         print(new_user_data)
#         new_user = await db.users.add(new_user_data)
#         await db.commit()
#     print(f"{new_user=}")
#     print("!!!")
#     assert new_user