class JWTPublicKeyNotFound(Exception):
    def __init__(self):
        super().__init__(f"Public key not found.")
