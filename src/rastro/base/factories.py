from typing import ParamSpec, Protocol, TypeVar

P = ParamSpec("P")
T_CO = TypeVar("T_CO", covariant=True)


class Factory(Protocol[P, T_CO]):
    def create(self, *args: P.args, **kwargs: P.kwargs) -> T_CO: ...
