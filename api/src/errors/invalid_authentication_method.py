class InvalidAuthenticationMethodError(Exception):
    def __init__(self):
        super().__init__(f"Invalid authentication method.")
