# 1: must have a code
# 2: code must be unique across all instances
# 3: code must be snake uppercased


import pytest

from rastro_base.error import (
    BaseError,
    CodeDuplicatedError,
    CodeNamingError,
    CodeUndefinedError,
)


def test_error_subclassing_fails_when_no_code_is_provided() -> None:
    with pytest.raises(CodeUndefinedError):

        class _(BaseError):
            pass


def test_error_code_must_be_unique() -> None:
    with pytest.raises(CodeDuplicatedError):

        class _1(BaseError):
            code = "ERROR_ONE"

        class _1_again(BaseError):
            code = "ERROR_ONE"


def test_error_code_must_be_snakeuppercased() -> None:
    with pytest.raises(CodeNamingError):

        class _(BaseError):
            code = "notuppersnakecased"


def test_valid_error_code_registry_state() -> None:
    class _1(BaseError):
        code = "VALID_ERROR_CODE_ONE"

    class _2(BaseError):
        code = "VALID_ERROR_CODE_TWO"

    assert _1.code == "VALID_ERROR_CODE_ONE"
    assert _2.code == "VALID_ERROR_CODE_TWO"


def test_error_initialization() -> None:
    class TestError(BaseError):
        code = "TEST_ERROR"

    test_error = TestError(title="title", details={"foo": "bar"})

    details = test_error.details

    assert test_error.title == "title"
    assert details is not None
    assert details["foo"] == "bar"
