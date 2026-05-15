import pytest

from rastro_shared_kernel.env import get_env


def test_get_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("MOCK", "mock")
    env = get_env("MOCK")

    assert env == "mock"


def test_get_env_none(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MOCK", raising=False)
    env = get_env("MOCK")

    assert env is None


def test_get_env_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("MOCK", raising=False)
    env = get_env("MOCK", default="default_mock")

    assert env == "default_mock"
