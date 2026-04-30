import re
import unicodedata
from typing import Annotated

from pydantic import AfterValidator, StringConstraints

from rastro_base.value_object import RootValueObject

# https://emailregex.com/
EMAIL_PATTERN = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
UNICODE_USERNAME_PATTERN = re.compile(r"^[\w.@+-]+\Z")


class Email(
    RootValueObject[
        Annotated[
            str,
            StringConstraints(
                to_lower=True, strip_whitespace=True, pattern=EMAIL_PATTERN
            ),
        ]
    ]
): ...


class Username(
    RootValueObject[
        Annotated[
            str,
            AfterValidator(lambda val: unicodedata.normalize("NFKC", val)),
            StringConstraints(pattern=UNICODE_USERNAME_PATTERN),
        ]
    ]
): ...


class RawPassword(
    RootValueObject[
        Annotated[
            str,
            StringConstraints(min_length=8),
        ]
    ]
): ...


class HashedPassword(RootValueObject[str]): ...
