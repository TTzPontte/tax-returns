from dataclasses import dataclass
from typing import List

from layers.common.Models.client import GqlClient
from layers.common.Models.dao import AppSyncDao
from src.TaxReturnsSendEmail.Builder.EmailConfig import EmailConfig
from src.TaxReturnsSendEmail.Builder.html_builder import HtmlBuilder


@dataclass
class EmailToSend:
    sku: str
    email: str
    contractinfoID: List[str]


def create_email_from_record(record):
    return EmailToSend(
        sku=record.get('documentNumber'),
        email=record.get('email'),
        contractinfoID=record.get('contractinfoID')
    )


@dataclass
class Facade:
    email_list: List[EmailToSend] = None

    def __post_init__(self):
        self.email_list = []

    def process_records(self, cpf_or_cnpj):
        print(cpf_or_cnpj)
        gql_client = GqlClient()
        dao = AppSyncDao(gql_client)

        result = dao.get_records_by_document_number(document_number=cpf_or_cnpj)
        items = result.get('listParticipants', {}).get('items', [])

        self.email_list = [create_email_from_record(record) for record in items]
        print(self.email_list)

def send_single(self, output_file: str):
    for email_to_send in self.email_list:
        config = EmailConfig(to_email=email_to_send.email)
        email_service = HtmlBuilder(config=config, html_file_path=None, output_file=output_file)
        soup = email_service.parse_html()
        modified_html = email_service.modify_html_single(soup, link=email_to_send.links[0])
        email_service.save_modified_html_to_file(modified_html)
        emails = [email_to_send.email]
        email_service.send_emails(modified_html, emails)


#    def send_multiple(self, output_file: str):
#        for email_to_send in self.email_list:
#            config = EmailConfig(to_email=email_to_send.email)
#            email_service = HtmlBuilder(config=config, html_file_path=None, output_file=output_file)
#            soup = email_service.parse_html()
#            modified_html = email_service.modify_html_multiple(soup, links=email_to_send.links)
#            email_service.save_modified_html_to_file(modified_html)
#            emails = [email_to_send.email]
#            email_service.send_emails(modified_html, emails)

def lambda_handler(event, context):
    cpf_or_cnpj = event.get('cpf_or_cnpj')

    facade = Facade()
    facade.process_records(cpf_or_cnpj)

    output_file = '/path/to/output/email_output.html'
    # facade.send_single(output_file)


if __name__ == "__main__":
    cpf_or_cnpj_input = '22308464852'

    facade_instance = Facade()
    facade_instance.process_records(cpf_or_cnpj_input)

    output_file_path = '/path/to/output/email_output.html'
    #  facade_instance.send_single(output_file_path)
    #  facade_instance.send_multiple(output_file_path)
