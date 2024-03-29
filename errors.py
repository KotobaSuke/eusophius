class OverlengthError(BaseException):
    ...


class ArgMissingError(BaseException):
    ...


class EmptyMsgError(BaseException):
    ...


class OptError(BaseException):

    def __init__(self, opts: list) -> None:
        self.opts = opts


class OptConflictError(BaseException):

    def __init__(self, cause: str, conf: list[str]) -> None:
        self.cause = cause
        self.conf = conf


class UnsupportedGameError(BaseException):
    ...
