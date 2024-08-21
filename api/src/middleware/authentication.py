import jwt.algorithms
import requests
import jwt
from config.environment import environment
from tornado.web import HTTPError
from errors.jwt_public_key_not_found import JWTPublicKeyNotFound
from errors.invalid_authentication_method import InvalidAuthenticationMethodError
from models.authentication_provider_enum import AuthenticationProvider


class Authentication(object):
    def __init__(self, method) -> None:
        if method != "jwt":
            raise InvalidAuthenticationMethodError()
        self.authentication_method = method

    def __call__(self, handler_class) -> None:
        def wrap_execute(handler_execute):
            def require_auth(handler, kwargs):
                auth_header = handler.request.headers.get("Authorization", None)
                token = auth_header[7:]
                match environment.AUTHENTICATION_PROVIDER:
                    case AuthenticationProvider.COGNITO:
                        if not self.__verify_cognito_token(token):
                            raise HTTPError(401, reason="Invalid token")
                    case AuthenticationProvider.POCKETBASE:
                        if not self.__verify_pocketbase_token(token):
                            raise HTTPError(401, reason="Invalid token")
                return handler_execute(handler, kwargs)

            return require_auth

        handler_class._execute = wrap_execute(handler_class._execute)
        return handler_class

    def __download_jwks(self, provider: AuthenticationProvider) -> dict:
        """
        Downloads the JSON Web Key Set (JWKS) from the authentication provider
        :param provider: The authentication provider
        :return: The JWKS as a dictionary
        """
        match provider:
            case AuthenticationProvider.COGNITO:
                url = f"https://cognito-idp.{environment.COGNITO_REGION}.amazonaws.com/{environment.COGNITO_USER_POOL_ID}/.well-known/jwks.json"
            case AuthenticationProvider.POCKETBASE:
                raise NotImplementedError()
        return requests.get(url).json()

    def __get_public_key(self, kid: str, jwks: dict):
        """
        Gets the public key from the JWKS
        :param kid: The key ID
        :param jwks: The JSON Web Key Set
        :return: The public key
        """
        for key in jwks["keys"]:
            if key["kid"] == kid:
                public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key)
                return public_key
        raise JWTPublicKeyNotFound()

    def __verify_pocketbase_token(self, token: str) -> bool:
        """
        Verifies the PocketBase token
        :param token: The token
        :return: True if the token is valid, False otherwise
        """
        try:
            response = requests.post(
                f"{environment.POCKETBASE}/api/auth/token-validate",
                headers={"Authorization": f"{token}"},
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def __verify_cognito_token(self, token: str) -> bool:
        """
        Verifies the Cognito token
        :param token: The token
        :return: True if the token is valid, False otherwise
        """
        jwks = self.__download_jwks(AuthenticationProvider.COGNITO)
        header = jwt.get_unverified_header(token)
        public_key = self.__get_public_key(header["kid"], jwks)
        try:
            jwt.decode(
                token,
                public_key,
                algorithms=["RS256"],
                audience=environment.COGNITO_AUDIENCE,
            )
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False
