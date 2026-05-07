from rastro.auth.domain.services import PasswordHashingService
from rastro.auth.domain.value_objects import (
    Email,
    HashedPassword,
    RawPassword,
    Username,
)
from rastro_base.aggregate import AggregateRoot
from rastro_shared_kernel.value_objects import Id


class User(AggregateRoot):
    id: Id
    username: Username
    email: Email
    password: HashedPassword
    is_active: bool

    def set_password(
        self,
        raw_password: RawPassword,
        password_hashing_service: PasswordHashingService,
    ) -> None:
        self.password = password_hashing_service.hash(raw_password)

    def verify_password(
        self,
        raw_password: RawPassword,
        password_hashing_service: PasswordHashingService,
    ) -> tuple[bool, bool]:
        is_password_correct, must_upgrade_hash = password_hashing_service.verify(
            raw_password, self.password
        )

        if must_upgrade_hash:
            self.set_password(raw_password, password_hashing_service)

        return is_password_correct, must_upgrade_hash
