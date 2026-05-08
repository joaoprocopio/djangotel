from rastro_base.error import BaseError


class CredenciaisIncorretasError(BaseError):
    code = "AUTH_CREDENCIAIS_INCORRETAS"


class ContaNaoEncontradaError(BaseError):
    code = "AUTH_CONTA_NAO_ENCONTRAR"
