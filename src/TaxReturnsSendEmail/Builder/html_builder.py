import io
from dataclasses import dataclass, field
from typing import List

from bs4 import BeautifulSoup

from .EmailConfig import EmailConfig
from .helper import create_tr_html, find_buttons, create_button_html


def find_table(soup: BeautifulSoup):
    return soup.find('tbody', class_='table-items-list')


@dataclass
class HtmlBuilder:
    config: EmailConfig
    html_file_path: str
    output_file: str
    links: List[str] = field(default_factory=list)

    def parse_html(self, html_string: str) -> BeautifulSoup:
        return BeautifulSoup(html_string, 'html.parser')

    def modify_html_multiple(self, soup: BeautifulSoup, links: List[str]) -> str:
        table = find_table(soup)
        for index, link in enumerate(links):
            button_template = create_tr_html(link, index + 1)
            new_button = BeautifulSoup(button_template, 'html.parser')
            table.append(new_button)
        return str(soup)

    def modify_html_single(self, soup: BeautifulSoup, links: List) -> str:
        link = links[0]
        for button in find_buttons(soup):
            button_html = create_button_html(link)
            new_button = BeautifulSoup(button_html, 'html.parser').button
            button.replace_with(new_button)
        return str(soup)

    def save_modified_html_to_file(self, modified_html: str) -> None:
        html_file = io.StringIO()
        html_file.write(modified_html)
        return html_file

    def send_email(self, modified_html: str) -> None:
        self.config.send_email(modified_html)

    def send_emails(self, modified_html: str, emails) -> None:
        self.config.send_emails(modified_html, emails)


if __name__ == '__main__':
    output_file = '/home/matheus/Documents/work/portal-scripts/src/TaxReturns/email/html/email_output.html'
    input_file = '/home/matheus/Documents/work/portal-scripts/src/TaxReturns/email/html/single_email__.html'
    from_email = 'lucas@pontte.com.br'

    config = EmailConfig(from_email=from_email)
    email_service = HtmlBuilder(config, input_file, output_file)
    soup = email_service.parse_html()
    modified_html = email_service.modify_html_multiple(soup, links=[
        "https://ir-tax-returns.s3.amazonaws.com/ir-tax-returns/ir-2023/IR_2022_129241.pdf",
        "https://ir-tax-returns.s3.amazonaws.com/ir-tax-returns/ir-2023/IR_2022_129243.pdf",
        "https://ir-tax-returns.s3.amazonaws.com/ir-tax-returns/ir-2023/IR_2022_129244.pdf",
        "https://ir-tax-returns.s3.amazonaws.com/ir-tax-returns/ir-2023/IR_2022_129246.pdf",
        "https://ir-tax-returns.s3.amazonaws.com/ir-tax-returns/ir-2023/IR_2022_129248.pdf",
        "https://ir-tax-returns.s3.amazonaws.com/ir-tax-returns/ir-2023/IR_2022_129249.pdf",
    ])
    email_service.save_modified_html_to_file(modified_html)
    emails = [from_email, 'silvio.junior@pontte.com.br', 'evandro@pontte.com.br']
    #email_service.send_emails(modified_html, emails)
