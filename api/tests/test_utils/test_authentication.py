import pytest
from unittest.mock import patch, Mock
from jwt import ExpiredSignatureError, InvalidTokenError
from tornado.web import HTTPError

import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from src.middleware.authentication import Authentication, JWTProvider
from src.errors.jwt_public_key_not_found import JWTPublicKeyNotFound
from src.errors.invalid_authentication_method import InvalidAuthenticationMethodError
from src.config.environment import environment

# Mock environment variables
mock_environment = {
    "COGNITO_AUDIENCE": "audience",
    "COGNITO_REGION": "region",
    "COGNITO_USER_POOL_ID": "user_pool_id",
}

# Mock JWKS data
mock_jwks = {
    "keys": [
        {
            "kid": "test_kid",
            # ... other necessary JWKS key data ...
        }
    ]
}

# Mock JWT token
mock_token = "header.payload.signature"
mock_unverified_header = {"kid": "test_kid"}


# Mock handler class
class MockHandlerClass:
    request = Mock(headers={"Authorization": f"Bearer {mock_token}"})


@pytest.fixture
def auth_instance():
    with patch("environment", mock_environment):
        with patch("requests.get", return_value=Mock(json=lambda: mock_jwks)):
            auth = Authentication(method="jwt")
    return auth


def test_authentication_success(auth_instance):
    with patch("jwt.decode") as mock_decode:
        with patch("jwt.get_unverified_header", return_value=mock_unverified_header):
            auth_instance(MockHandlerClass)
            mock_decode.assert_called_once()


def test_authentication_failure_expired_token(auth_instance):
    with patch("jwt.decode", side_effect=ExpiredSignatureError):
        with patch("jwt.get_unverified_header", return_value=mock_unverified_header):
            with pytest.raises(HTTPError) as exc_info:
                auth_instance(MockHandlerClass)
            assert exc_info.value.status_code == 401
            assert exc_info.value.reason == "Token has expired"


def test_authentication_failure_invalid_token(auth_instance):
    with patch("jwt.decode", side_effect=InvalidTokenError):
        with patch("jwt.get_unverified_header", return_value=mock_unverified_header):
            with pytest.raises(HTTPError) as exc_info:
                auth_instance(MockHandlerClass)
            assert exc_info.value.status_code == 401
            assert exc_info.value.reason == "Invalid token"


def test_authentication_failure_public_key_not_found(auth_instance):
    with patch("jwt.get_unverified_header", return_value=mock_unverified_header):
        with pytest.raises(JWTPublicKeyNotFound):
            auth_instance(MockHandlerClass)


def test_invalid_authentication_method():
    with pytest.raises(InvalidAuthenticationMethodError):
        Authentication(method="invalid_method")
