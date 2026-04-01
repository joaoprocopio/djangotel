from dataclasses import dataclass
from typing import Self

from rastro_base.error import InvalidIdError
from rastro_base.value_object import ValueObject
from rastro_shared_kernel.mixins import Validate


@dataclass(frozen=True)
class Id(ValueObject, Validate):
    value: int

    def validate(self) -> Self:
        if self.value < 1:
            raise InvalidIdError()

        return self
