from rastro.auth.domain.value_objects import Email, HashedPassword, Username
from rastro_base.entity import Entity
from rastro_shared_kernel.value_objects import Id


class User(Entity[Id]):
    username: Username
    email: Email
    hashed_password: HashedPassword
    is_active: bool
