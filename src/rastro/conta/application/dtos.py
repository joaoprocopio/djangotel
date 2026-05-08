from rastro.conta.domain.value_objects import (
    Email,
    HashedPassword,
    RawPassword,
    Username,
)
from rastro_base.dto import DTO
from rastro_shared_kernel.value_objects import Id


class SignUpInput(DTO):
    username: Username
    email: Email
    password: RawPassword


class SignInInput(DTO):
    query: Email | Username
    password: RawPassword


class UserOutput(DTO):
    id: Id
    email: Email
    username: Username
    password: HashedPassword
    is_active: bool


class UserPublic(DTO):
    email: Email
    username: Username
