from enum import Enum
import jwt.algorithms
import requests
import jwt
from config.environment import environment
from tornado.web import HTTPError
from errors.jwt_public_key_not_found import JWTPublicKeyNotFound
from errors.invalid_authentication_method import InvalidAuthenticationMethodError


class JWTProvider(Enum):
    COGNITO = "cognito"
    POCKETBASE = "pocketbase"


class Authentication(object):
    def __init__(self, method) -> None:
        if method != "jwt":
            raise InvalidAuthenticationMethodError()
        self.authentication_method = method
        self.jwks = self.__download_jwks(JWTProvider.COGNITO)

    def __call__(self, handler_class) -> None:
        def wrap_execute(handler_execute):
            def require_auth(handler, kwargs):
                auth_header = handler.request.headers.get("Authorization", None)
                token = auth_header[7:]
                try:
                    header = jwt.get_unverified_header(token)
                    public_key = self.__get_public_key(header["kid"])
                    print(public_key)
                    jwt.decode(
                        token,
                        public_key,
                        algorithms=["RS256"],
                        audience=environment.COGNITO_AUDIENCE,
                    )
                except jwt.ExpiredSignatureError:
                    raise HTTPError(401, reason="Token has expired")
                except jwt.InvalidTokenError as e:
                    raise HTTPError(401, reason="Invalid token")
                return handler_execute(handler, kwargs)

            return require_auth

        handler_class._execute = wrap_execute(handler_class._execute)
        return handler_class

    def __download_jwks(self, provider: JWTProvider) -> dict:
        match provider:
            case JWTProvider.COGNITO:
                url = f"https://cognito-idp.{environment.COGNITO_REGION}.amazonaws.com/{environment.COGNITO_USER_POOL_ID}/.well-known/jwks.json"
            case JWTProvider.POCKETBASE:
                raise NotImplementedError()
        return requests.get(url).json()

    def __get_public_key(self, kid: str):
        for key in self.jwks["keys"]:
            if key["kid"] == kid:
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
                return public_key
        raise JWTPublicKeyNotFound()
