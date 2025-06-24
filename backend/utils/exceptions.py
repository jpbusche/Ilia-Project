class CostumerException(Exception):
    pass

class AuthException(Exception):
    
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code