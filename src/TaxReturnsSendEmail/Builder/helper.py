from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup


def find_buttons(soup: BeautifulSoup):
    return soup.find_all('button')



def create_button_html(link) -> str:

    button_html = f'''
    <button
  style="
    background-color: inherit !important;
    border: none;
    text-decoration-color: white;
  "
  class="mcnButtonContent"
  onclick="window.open('{link}', '_blank');"
>
  <a
    class="mcnButton"
    style="
      font-weight: bold;
      letter-spacing: normal;
      line-height: 100%;
      text-align: center;
      text-decoration: none;
      color: #ffffff;
      mso-line-height-rule: exactly;
      -ms-text-size-adjust: 100%;
      -webkit-text-size-adjust: 100%;
      display: block;
    "
    title="Acessar meu demonstrativo"
    href="{link}"
    target="_blank"
  >
    Acessar meu demonstrativo
  </a>
</button>

    '''
    return button_html


def create_tr_html(link: str, number: int) -> str:
    class_name = 'table-item-even' if number % 2 == 0 else 'table-item-odd'
    return f''' 
    <tr>
        <td class="{class_name}"><a href="{link}"> Demonstrativo {number}</a></td>
    </tr>'''

@dataclass
class EmailToSend:
    sku: str
    email: str
    links: List[str]

