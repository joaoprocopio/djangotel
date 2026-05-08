from abc import ABC, abstractmethod
from typing import Optional

from rastro.conta.domain.aggregates import Conta
from rastro.conta.domain.value_objects import Email, HashedPassword, Username
from rastro_shared_kernel.value_objects import Id


class ContaRepository(ABC):
    @abstractmethod
    def create(
        self, username: Username, email: Email, hashed_password: HashedPassword
    ) -> Conta: ...

    @abstractmethod
    def get_by_id(self, id: Id) -> Optional[Conta]: ...

    @abstractmethod
    def get_by_email(self, email: Email) -> Optional[Conta]: ...

    @abstractmethod
    def get_by_username(self, username: Username) -> Optional[Conta]: ...

    @abstractmethod
    def update_password(self, user: Conta) -> Conta: ...
