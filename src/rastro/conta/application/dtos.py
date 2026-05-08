from rastro.conta.domain.value_objects import (
    Email,
    HashedPassword,
    RawPassword,
    Username,
)
from rastro_base.dto import DTO
from rastro_shared_kernel.value_objects import Id


class CadastrarInput(DTO):
    username: Username
    email: Email
    password: RawPassword


class EntrarInput(DTO):
    query: Email | Username
    password: RawPassword


class ContaOutput(DTO):
    id: Id
    email: Email
    username: Username
    password: HashedPassword
    is_active: bool


class ContaPublic(DTO):
    email: Email
    username: Username
