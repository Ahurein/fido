class NotFoundException(Exception):
    def __init__(self, message = "Resource not found"):
        super().__init__(message)