class ZCException(Exception):
    def __init__(self, error_code, error_message):
        super().__init__((error_code, error_message))
        self.error_message = error_message
        self.error_code = error_code
        self._error_message = error_message

    def __str__(self):
        return {"error_code": str(self.error_code), "error_message": repr(self.error_message)}

    @property
    def message(self):
        return self.error_message

    @property
    def code(self):
        return self.error_code

    def format(self, *args, **kwargs):
        self.error_message = self._error_message.format(*args, **kwargs)
        return self
