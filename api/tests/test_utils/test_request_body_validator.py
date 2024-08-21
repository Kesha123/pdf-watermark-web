import os
import sys
import pytest
from dataclasses import dataclass
from tornado.web import RequestHandler, HTTPError

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from src.utils.request_body_validator import request_body_validator


@dataclass
class SampleData:
    field1: str
    field2: int


class MockRequestHandler(RequestHandler):
    def __init__(self, request_body):
        self.request = type("obj", (object,), {"body": request_body})
        self.data = None


def test_valid_json_body():
    @request_body_validator(SampleData)
    def sample_handler(handler, *args, **kwargs):
        return handler.data

    handler = MockRequestHandler(b'{"field1": "value1", "field2": 123}')
    result = sample_handler(handler)
    assert result.field1 == "value1"
    assert result.field2 == 123


def test_invalid_json_body():
    @request_body_validator(SampleData)
    def sample_handler(handler, *args, **kwargs):
        return handler.data

    handler = MockRequestHandler(b"invalid json")
    with pytest.raises(HTTPError) as excinfo:
        sample_handler(handler)
    assert excinfo.value.status_code == 400


def test_json_body_cannot_convert_to_dataclass():
    @request_body_validator(SampleData)
    def sample_handler(handler, *args, **kwargs):
        return handler.data

    handler = MockRequestHandler(b'{"field1": "value1"}')
    with pytest.raises(HTTPError) as excinfo:
        sample_handler(handler)
    assert excinfo.value.status_code == 400


def test_non_dataclass_parameter():
    with pytest.raises(TypeError):

        @request_body_validator(dict)
        def sample_handler(handler, *args, **kwargs):
            return handler.data
