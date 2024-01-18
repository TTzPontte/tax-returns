# ./src/main.py

from dataclasses import field, dataclass
from IR import parse_json
from helpers.aztronic import get_ir, get_data
from Models.client import GqlClient
from Models.dao import TaxReturnsFacade


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
        for id_ in self.id_list:
            print("---", id_, "---")
            self._current_id = str(id_)
            ir = get_ir(self._current_id)
            info = get_data(self._current_id, 'getFinances')
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

            gql_client = GqlClient()

            dao = TaxReturnsFacade(gql_client)
            dao.create_contract_info_with_participants_and_with_installments(current_pdf_info)

def lambda_handler(event, context):
    az_contract_id = event
    facade = Facade(az_contract_id)
    facade.process()
    facade.make_data()
    return {
        'statusCode': 200,
        'body': 'Lambda execution completed successfully.'
    }

# if __name__ == '__main__':
#     x = lambda_handler({'body': {
#         'contractId': '129246'
#     }}, {})
