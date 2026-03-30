from rastro_base.error import BaseError


class AuthenticationError(BaseError):
    code = "AUTH_AUTHENTICATION_FAILED"


class UserNotFoundError(BaseError):
    code = "AUTH_USER_NOT_FOUND"


class InvalidPasswordError(BaseError):
    code = "AUTH_INVALID_PASSWORD_ERROR"


class InvalidUsernameError(BaseError):
    code = "AUTH_INVALID_USERNAME_ERROR"


class InvalidEmailError(BaseError):
    code = "AUTH_INVALID_EMAIL_ERROR"
