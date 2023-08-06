class ParsingError(Exception):
    def __init__(self, message, validation_func, coercer):
        super().__init__(message)
        self.message = message
        self.validation_func = validation_func
        self.coercer = coercer

    def json(self):
        return {
            'Error': self.message,
            'ValidationFunction': self.validation_func,
            'Coercer': self.coercer
        }

    def __str__(self):
        return f"ParsingError: {self.message}, ValidationFunction: {self.validation_func}, Coercer: {self.coercer}"
