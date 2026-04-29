from app.core.messages import AuthMessages, UserMessages


class AppError(Exception):
    """Base Exception"""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code


class UserNotFoundError(AppError):
    def __init__(self, user_id: int | None = None):
        super().__init__(f"{UserMessages.NOT_FOUND}", 404)


class InvalidCredentialsError(AppError):
    def __init__(self):
        super().__init__(f"{AuthMessages.INVALID_CREDENTIALS}", 401)


class UnauthorizedError(AppError):
    def __init__(self):
        super().__init__(f"{AuthMessages.UNAUTHROIZED}", 401)


class UserAlreadyExistsError(AppError):
    def __init__(self):
        super().__init__(f"{UserMessages.ALREADY_EXISTS}", 409)


class InactiveUserError(AppError):
    def __init__(self):
        super().__init__(f"{UserMessages.INACTIVE}", 403)
