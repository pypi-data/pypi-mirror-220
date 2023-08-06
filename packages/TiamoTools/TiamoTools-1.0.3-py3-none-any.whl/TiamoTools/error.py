class BaseError(Exception):
    def __init__(self, error_info):
        super().__init__(self)
        self.error_info = error_info

    def __str__(self):
        return self.error_info


class ParamsError(BaseError):
    ...


class TargetError(BaseError):
    pass


class ClientError(BaseError):
    ...


class InitDBError(BaseError):
    ...
