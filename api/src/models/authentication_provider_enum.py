from enum import Enum


class AuthenticationProvider(Enum):
    COGNITO = "cognito"
    POCKETBASE = "pocketbase"
