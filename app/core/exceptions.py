class AppError(Exception):
    """Base Exception"""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code


class UserNotFoundError(AppError):
    def __init__(self, user_id: int):
        super().__init__(f"User with id {user_id} not found", 404)


class InvalidCredentialsError(AppError):
    def __init__(self):
        super().__init__("Email or password incorrect", 401)


class InactiveUserError(AppError):
    def __init__(self):
        super().__init__("This account has been deactivated", 403)
