import json
import logging
from http import HTTPStatus

from app import lambda_handler
from layers.common.config import LOGGING_LEVEL
from layers.common.errors import Errors, AppException

from layers.common.handlerbase import Result, Handler

logger = logging.getLogger(__name__)
logger.setLevel(LOGGING_LEVEL)

class TaxReturns(Handler):
    def pre_process(self):
        if self.event["body"]:
            self.event["body"] = json.dumps(self.event["body"])

    def validate(self):
        body = self.event["body"]
        properties = ["contractId"]
        errors = [prop for prop in properties if prop not in body]
        if errors:
            logger.debug('as propriedades %s nao foram enviadas', ', '.join(errors))
            raise AppException(Errors.PROPERTIES_MISSING, properties=",".join(errors))

    def handler(self):
        data = json.loads(self.event["body"])
        data_parsed = json.loads(data)
        contract_id = data_parsed.get("contractId")
        if contract_id:
            execution = lambda_handler(contract_id, {})

        if execution is not None:
            return Result(HTTPStatus.OK, execution)
        else:
            logger.debug('[TAX-RETURN][ERROR]: ', execution)
            return Result(HTTPStatus.INTERNAL_SERVER_ERROR,
                          {"message": f'Problem Getting Renegotiation: {contract_id}'})


def handler(event, context):
    return TaxReturns(event, context).run()


# if __name__ == '__main__':
#     x = handler({"body": {"contractId": "129246"}}, {})
