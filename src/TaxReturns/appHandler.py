import json
import logging
from http import HTTPStatus

import src.layers.common.config

from src.layers.common.handlerbase import Handler, Result
from src.layers.common.errors import AppException, Errors
from src.TaxReturns.app import lambda_handler
from daos import AztronicDao

logger = logging.getLogger(__name__)
logger.setLevel(src.layers.common.config.LOGGING_LEVEL)


class TaxReturns(Handler):
    def pre_process(self):
        print(self.event["body"])
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
        self.event["body"] = json.loads(self.event["body"])
        body = self.event["body"]
        contract_id = body.get("contractId")

        execution = lambda_handler(contract_id, {})
        if execution is not None:
            return Result(HTTPStatus.OK, execution)
        else:
            logger.debug('[TAX-RETURN][ERROR]: ', execution)
            return Result(HTTPStatus.INTERNAL_SERVER_ERROR,
                          {"message": f'Problem Getting Renegotiation: {contract_id}'})


def handler(event, context):
    print('bora')
    return TaxReturns(event, context).run()


if __name__ == '__main__':
    x = handler({"body": {"contractId": "129246"}}, {})

print(x)
