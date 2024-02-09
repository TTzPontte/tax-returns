from dataclasses import dataclass
from typing import List

import multiple_page
import single_page
import json

from Builder.EmailConfig import EmailConfig
from Builder.html_builder import HtmlBuilder


@dataclass
class EmailToSend:
    sku: str
    email: str
    contractinfoID: List[str]
    links: List[str]


def create_email_from_record(record):
    return EmailToSend(
        sku=record.get('documentNumber'),
        email=record.get('email'),
        contractinfoID=record.get('contractinfoID'),
        links=record.get('url')
    )


@dataclass
class Facade:
    email_list: List[EmailToSend] = None

    def __post_init__(self):
        self.email_list = []

    def send_single(self, input_file_path: str, output_file: str, links, email):
        email_list = [email]

        for email_to_send in email_list:
            config = EmailConfig(to_email=email_to_send)
            email_service = HtmlBuilder(config=config, html_file_path=input_file_path, output_file=output_file)
            soup = email_service.parse_html(html_string=input_file_path)
            modified_html = email_service.modify_html_single(soup, links=links)
            email_service.save_modified_html_to_file(modified_html)
            emails = [email_to_send]
            email_service.send_emails(modified_html, emails)

    def send_multiple(self, input_file_path: str, output_file: str, links, email):
        email_list = [email]
        for email_to_send in email_list:
            config = EmailConfig(to_email=email_to_send)
            email_service = HtmlBuilder(config=config, html_file_path=input_file_path, output_file=output_file)
            soup = email_service.parse_html(html_string=input_file_path)
            modified_html = email_service.modify_html_multiple(soup, links=links)
            email_service.save_modified_html_to_file(modified_html)
            emails = [email_to_send]
            print(emails)
            email_service.send_emails(modified_html, emails)

def lambda_handler(event, context):
    print(event)
    body_value = json.dumps(event)
    
    body_parsed = json.loads(body_value)
    print("BODY body_parsed:", body_parsed)

    body_data = body_parsed.get("body")
    print("Body Data:", body_data)

    links = body_data.get("links")
    email = body_data.get("email")

    print(links, email)
    facade = Facade()
    output_file_path = '/tmp/email_output.html'
    if len(links) > 1:
        input_file_path = multiple_page.html_content_multiple_page
        facade.send_multiple(input_file_path, output_file_path, links, email)
    else:
        input_file_path = single_page.html_content_single_page
        facade.send_single(input_file_path, output_file_path, links, email)


if __name__ == "__main__":
    facade_instance = Facade()
    input_file_path = '/home/matheus/Documents/fix/tax-returns/src/TaxReturnsSendEmail/html/single_email.html'
    output_file_path = '/home/matheus/Documents/fix/tax-returns/src/TaxReturnsSendEmail/html/email_output.html'
    body = json.dumps({
        "email": "matheus.santos@pontte.com.br",
        "links": [
            "https://ir-tax-returns.s3.amazonaws.com/ir-tax-returns/ir-2023/IR_2022_129241.pdf",
        ]
    })

    event = {"body": body}

    lambda_handler(event, {})
