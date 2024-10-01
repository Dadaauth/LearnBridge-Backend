class MyValueError(ValueError):
    def __init__(self, message: str, error_code: int) -> None:
        super().__init__(message)
        self.error_code = error_code


class Error:

    def __init__(self, code, message):
        self.code = code
        self.message = message