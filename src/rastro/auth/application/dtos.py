from dataclasses import dataclass

from rastro_base.dto import DTO
from rastro_shared_kernel.mixins import FromJson


@dataclass(frozen=True)
class SignUpInput(DTO, FromJson):
    username: str
    email: str
    password: str


@dataclass(frozen=True)
class SignInInput(DTO, FromJson):
    query: str
    password: str


@dataclass(frozen=True)
class UserOutput(DTO):
    id: int
    email: str
    username: str
    password: str
    is_active: bool
