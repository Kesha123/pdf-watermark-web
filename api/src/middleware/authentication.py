from tornado.web import HTTPError


class Authentication(object):
    def __init__(self, method) -> None:
        if method != "jwt":
            raise Exception("Invalid authentication method")
        self.authentication_method = method

    def __call__(self, handler_class) -> None:
        def wrap_execute(handler_execute):
            def require_auth(handler, kwargs):
                auth_header = handler.request.headers.get("Authorization", None)
                token = auth_header[7:]
                return handler_execute(handler, kwargs)

            return require_auth

        handler_class._execute = wrap_execute(handler_class._execute)
        return handler_class
