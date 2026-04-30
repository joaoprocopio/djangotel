import re
import unicodedata
from typing import Annotated

from pydantic import AfterValidator, StringConstraints

from rastro_base.value_object import ValueObject

# https://emailregex.com/
EMAIL_PATTERN = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
UNICODE_USERNAME_PATTERN = re.compile(r"^[\w.@+-]+\Z")


class Email(ValueObject):
    value: Annotated[
        str,
        StringConstraints(to_lower=True, strip_whitespace=True, pattern=EMAIL_PATTERN),
    ]


class Username(ValueObject):
    value: Annotated[
        str,
        AfterValidator(lambda val: unicodedata.normalize("NFKC", val)),
        StringConstraints(pattern=UNICODE_USERNAME_PATTERN),
    ]


class RawPassword(ValueObject):
    value: Annotated[
        str,
        StringConstraints(min_length=8),
    ]


class HashedPassword(ValueObject):
    value: str
