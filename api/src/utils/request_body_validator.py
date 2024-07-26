import json
from functools import wraps
from dataclasses import is_dataclass
from tornado.web import RequestHandler, HTTPError
from typing import Any, Callable, TypeVar, Type


F = TypeVar("F", bound=Callable[..., Any])


def request_body_validator(datacls: Type) -> Callable[[F], F]:
    """
    Validates the request body and creates an instance of the dataclass.
    :param datacls: The dataclass to validate the request body against.
    :return: The wrapped function.
    :raises TypeError: If the parameter is not a dataclass.
    :raises HTTPError: If the request body is not a valid JSON or the dataclass instance cannot be created.
    """
    if not is_dataclass(datacls):
        raise TypeError("The parameter must be a dataclass.")

    def process_request_body(func: F) -> F:
        @wraps(func)
        def wrapper(handler: RequestHandler, *args, **kwargs):
            try:
                body_data = json.loads(handler.request.body)
            except json.JSONDecodeError:
                raise HTTPError(400)
            try:
                request_body_instance = datacls(**body_data)
            except TypeError as e:
                raise HTTPError(400)
            handler.data = request_body_instance
            return func(handler, *args, **kwargs)

        return wrapper

    return process_request_body
