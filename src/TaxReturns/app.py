# ./src/main.py

from dataclasses import field, dataclass
from daos import AztronicDao
from IR import parse_json
# from env import API_TOKEN
# from helpers.PDF import generate_pdf
# from helpers.utils import csv_to_json


@dataclass
class Facade:
    az_contract_id: str
    _current_id: str = ''
    _ir_list: list = field(default_factory=list)
    response_list: list = field(default_factory=list)
    id_list: list = field(default_factory=list)

    def __post_init__(self):
        self.id_list = [self.az_contract_id]

    def process(self):
        aztronic_dao = AztronicDao()
        for id_ in self.id_list:
            print("---", id_, "---")
            self._current_id = str(id_)
            ir = aztronic_dao.get_ir(self._current_id)
            print(ir)
            info = aztronic_dao.get_data(self._current_id, 'getFinances')
            self._ir_list.append([ir, info])

    def make_data(self):
        for ir_info in self._ir_list:
            ir = ir_info[0]
            info = ir_info[1]
            print("---", info, "---")
            contrato = info['data']['posicaofinanceira']['contrato']
            ir = parse_json({
                "informeir": ir,
                "contrato": contrato
            })
            current_pdf = ir
            current_pdf_info = current_pdf.to_json()
            print("current_pdf_info", current_pdf_info)

    # def make_pdfs(self):
    #         b12 = generate_pdf([current_pdf_info], API_TOKEN)
    #         data = b12.get('data', {})
    #         url = data.get('url', "").split("?")[0]
    #         return_obj = {
    #             "url": url,
    #             "id": contrato.get('id_contrato'),
    #             "total": current_pdf_info['contractInfo'].get('SALDO'),
    #         }
    #         index = 0
    #         for email in current_pdf.emails:
    #             index += 1
    #             return_obj[f'participant_{index}'] = email
    #         self.response_list.append(return_obj)


def lambda_handler(event, context):
    az_contract_id = event.get('body').get('contractId')
    facade = Facade(az_contract_id)
    facade.process()
    return {
        'statusCode': 200,
        'body': 'Lambda execution completed successfully.'
    }

if __name__ == '__main__':
    x = lambda_handler({'body': {
        'contractId': '129246'
    }}, {})

    print(x)