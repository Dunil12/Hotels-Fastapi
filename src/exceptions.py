

class NabronirovalException(Exception):
    detail: str = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs): # real signature unknown
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"

class ObjectAlreadyExistException(NabronirovalException):
    detail = "Объект уже существует"

class CheckinDateLaterThanCheckoutDateException(NabronirovalException):
    detail = "Объект уже существует"

class AllRoomsBookedException(NabronirovalException):
    detail = "Все номера забронированы"


