import json
from handlers.base import BaseHandler
from middleware.authentication import Authentication
from swagger.get_health_model import GetHealthModel


@Authentication("jwt")
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
                  $ref: '#/definitions/GetHealthModel'
            400:
                description: Bad request
        """
        self.write(json.dumps({"status": "ok"}))
