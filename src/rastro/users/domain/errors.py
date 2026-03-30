from rastro.base.error import BaseError


class AuthenticationError(BaseError):
    code = "USERS_AUTHENTICATION_FAILED"


class UserNotFoundError(BaseError):
    code = "USERS_USER_NOT_FOUND"
