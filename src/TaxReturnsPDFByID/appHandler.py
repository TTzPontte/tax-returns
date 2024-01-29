import logging
from http import HTTPStatus


from app import invoke_lambda_function
from configFiles.config import LOGGING_LEVEL
from configFiles.errors import Errors, AppException
from configFiles.handlerbase import Result, Handler

logger = logging.getLogger(__name__)
logger.setLevel(LOGGING_LEVEL)


class TaxReturnsPDFbyId(Handler):
    def pre_process(self):
        if self.event['pathParameters'] and 'taxReturnId' in self.event['pathParameters']:
            self.event['taxReturnId'] = self.event['pathParameters']['taxReturnId']

    def validate(self):
        tax_return_id = self.event.get('taxReturnId')
        if tax_return_id is None:
            logger.debug('A propriedade taxReturnId não foi enviada')
            raise AppException(Errors.PROPERTIES_MISSING, properties="taxReturnId")
    def handler(self):
        tax_return_id = self.event.get('taxReturnId')

        print(tax_return_id)
        if tax_return_id:
           execution = invoke_lambda_function(tax_return_id)

        if execution is not None:
            return Result(HTTPStatus.OK, execution)
        else:
            logger.debug('[TAX-RETURN-PDF-BY-ID][ERROR]: ', execution)
            return Result(HTTPStatus.INTERNAL_SERVER_ERROR,
                          {"message": f'Problem Getting Tax Return: {tax_return_id}'})


def handler(event, context):
    print(event)
    return TaxReturnsPDFbyId(event, context).run()


if __name__ == '__main__':
    x = handler({
        "pathParameters": {
            "taxReturnId": "07ad7127-761a-4460-b515-40a15b09a61a"
        }
    }, {})
    print(handler)
