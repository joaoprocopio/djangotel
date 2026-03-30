from dataclasses import dataclass

from rastro.base.entities import Entity, Id
from rastro.users.value_objects import Email, Password, Username


@dataclass
class User(Entity[Id]):
    username: Username
    email: Email
    password: Password
