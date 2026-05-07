from rastro.auth.domain.services import PasswordHashingService, PasswordVerification
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
    ) -> PasswordVerification:
        verification = password_hashing_service.verify(raw_password, self.password)

        if verification.is_correct and verification.must_upgrade:
            self.set_password(raw_password, password_hashing_service)

        return verification
