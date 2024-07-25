import json
from tornado_swagger.model import register_swagger_model

import tornado.web

from handlers.base import BaseHandler
from middleware.authentication import Authentication


@Authentication('jwt')
class Health(BaseHandler):

    def get(self) -> None:
        """
        Description end-point

        ---
        tags:
        - Health Check
        summary: Check API
        produces:
        - application/json
        responses:
            200:
                description: Ok
                schema:
                  $ref: '#/definitions/GetHealth'
            400:
                description: Bad request
        """
        self.write(json.dumps({"status": "ok"}))


@register_swagger_model
class GetHealth:
    """
    ---
    type: object
    properties:
        status:
            type: string
            example: "ok"
    """
