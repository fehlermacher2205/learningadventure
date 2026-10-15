class AppError(Exception):
    """Base exception for the application."""
    
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class PermissionDeniedError(AppError):
    pass


class ValidationError(AppError):
    pass


class DatabaseError(AppError):
    pass


class ObjectNotFoundError(AppError):
    pass
class SessionExpiredError(AppError):
    pass
class UnauthorizedError(AppError):
    pass
class JSONParsingError(AppError):
    pass
class InvalidSessionError(AppError):
    pass