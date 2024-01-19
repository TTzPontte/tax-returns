"""Objetos base para os handlers."""

import decimal
import json
import logging
from dataclasses import dataclass
from http import HTTPStatus

from . import errors
from .config import LOGGING_LEVEL, AWS_SAM_LOCAL


logger = logging.getLogger(__name__) # pylint: disable=invalid-name
logger.setLevel(LOGGING_LEVEL)

def convert_header_lowercase(event: object):
    """Converte os nomes dos cabeçalhos para minúsculo.

    Args:
        event: o evento recebido do API Gateway.
    """

    if "headers" in event:
        headers = {k.lower():v for k, v in event["headers"].items()}
        event["headers"] = headers

    if "multiValueHeaders" in event:
        headers = {k.lower():v for k, v in event["multiValueHeaders"].items()}
        event["multiValueHeaders"] = headers

class CustomEncoder(json.JSONEncoder):
    """Codificador para o JSON.

    Transforma o Decimal em números.
    """
    def default(self, o):  # pylint: disable=E0202
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            return int(o)
        return super(CustomEncoder, self).default(o)

@dataclass
class Result():
    """Classe para indicação do resultado."""

    status_code: HTTPStatus
    obj: dict

    def answer(self) -> object:
        """Retorna o resultado para o API Gateway.

        Returns:
            Objeto com as informações que o API Gateway aguarda.
        """
        data = {
            "statusCode": self.status_code,
            "headers": {
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
                "Access-Control-Allow-Origin": "*",
            }
        }

        if self.obj:
            data["body"] = json.dumps(self.obj, cls=CustomEncoder)
            data["headers"]["Content-Type"] = "application/json"

        return data

class Handler():
    """Realiza o tratamento do evento do API Gateway"""

    def __init__(self, event, context):
        """Inicializa a classe de tratamento.

        Args:
            event: o evento recebido do API Gateway.
            context: o contexto recebido do API Gateway.
        """

        self._event = event
        convert_header_lowercase(self._event)

        self._context = context

    @property
    def event(self) -> object:
        """Retorna o evento do Handler.

        Returns:
            O evento recebido do API Gateway já tratado.
        """
        return self._event

    def aws_local_preprocess(self):
        """Realiza o pré processamento se estiver rodando em DEV."""

    def pre_process(self):
        """Realiza o pré processamento das informações."""

    def check_authorization(self):
        """Valida a autorização."""

    def validate(self):
        """Valida as informações enviadas"""

    def handler(self) -> Result:
        """Execução do handler do evento."""
        raise NotImplementedError()

    def run(self):
        """Executa o handler."""

        if AWS_SAM_LOCAL:
            logger.debug("AWS_SAM_LOCAL: %s", AWS_SAM_LOCAL)

        try:
            if AWS_SAM_LOCAL:
                self.aws_local_preprocess()

            self.pre_process()

            if not AWS_SAM_LOCAL:
                self.check_authorization()

            self.validate()

            res = self.handler()

            if not isinstance(res, Result):
                raise TypeError("handler result is not a Result")

            return res.answer()

        except errors.AppException as err:
            logger.error("execution exception received: %s", err, exc_info=1)
            res = err.as_result()
        except Exception as err: # pylint: disable=broad-except
            logger.critical("exception received: %s", err, exc_info=1)
            res = errors.AppException(errors.Errors.UNKNOWN).as_result()
        else:
            logger.critical("code did not return")
            res = errors.AppException(errors.Errors.RUNTIME,
                                      message="code did not return").as_result()

        return res.answer()