class NotFoundException(Exception):
    """ Not found exception """
    def __init__(self, message = "Resource not found"):
        super().__init__(message)