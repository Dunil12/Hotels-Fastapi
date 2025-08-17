from fastapi import HTTPException

class NabronirovalException(Exception):
    detail: str = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs): # real signature unknown
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"

class ObjectAlreadyExistException(NabronirovalException):
    detail = "Объект уже существует"

class RoomNotFoundException(ObjectNotFoundException):
    detail = "Номер не найден"

class HotelNotFoundException(ObjectNotFoundException):
    detail = "Отель не найден"

class CheckinDateLaterThanCheckoutDateException(NabronirovalException):
    detail = "Объект уже существует"

class AllRoomsBookedException(NabronirovalException):
    detail = "Все номера забронированы"




class NabronirovalHTTPExceptions(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(NabronirovalHTTPExceptions):
    status_code = 404
    detail = "Отель не найден"

class RoomNotFoundHTTPException(NabronirovalHTTPExceptions):
    status_code = 404
    detail = "Номер не найден"

class UserNotFoundHTTPException(NabronirovalHTTPExceptions):
    status_code = 404
    detail = "Пользователь не найден"

class CheckinDateLaterThanCheckoutDateHTTPException(NabronirovalHTTPExceptions):
    status_code = 400
    detail = "Дата заезда позже даты выезда"

class AllRoomsBookedHTTPException(NabronirovalException):
    status_code = 409
    detail = "Все номера забронированы"