from pydantic import PositiveInt

from rastro_base.value_object import ValueObject


class Id(ValueObject):
    value: PositiveInt
