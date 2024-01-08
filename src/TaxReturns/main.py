import pandas as pd
from dataclasses import field, dataclass
from IR import parse_json
from src.TaxReturns.helpers.PDF import generate_pdf
from src.TaxReturns.helpers.aztronic import get_ir, get_data
from src.TaxReturns.helpers.utils import csv_to_json


@dataclass
class Facade:
    _current_id: str = ''
    _ir_list: list = field(default_factory=list)
    response_list: list = field(default_factory=list)
    records: list = field(default_factory=list)
    id_list: list = field(default_factory=list)

    def __post_init__(self, input_document_path):
        self.records = csv_to_json(input_document_path)
        self.id_list = [record.get('Identificador do Contrato') for record in self.records if
                        record.get('Identificador do Contrato') is not None]

    def process(self):
        for id_ in self.id_list:
            print("---", id_, "---")
            self._current_id = str(id_)
            ir = get_ir(self._current_id)
            info = get_data(self._current_id, 'getFinances')
            self._ir_list.append([ir, info])

    def make_pdfs(self):
        for ir_info in self._ir_list:
            ir = ir_info[0]
            info = ir_info[1]
            contrato = info['data']['posicaofinanceira']['contrato']
            ir = parse_json({
                "informeir": ir,
                "contrato": contrato
            })
            current_pdf = ir
            current_pdf_info = current_pdf.to_json()
            print("current_pdf_info", current_pdf_info)
            b12 = generate_pdf([current_pdf_info], API_TOKEN)
            data = b12.get('data', {})
            url = data.get('url', "").split("?")[0]
            return_obj = {
                "url": url,
                "id": contrato.get('id_contrato'),
                "total": current_pdf_info['contractInfo'].get('SALDO'),
            }
            index = 0
            for email in current_pdf.emails:
                index += 1
                return_obj[f'participant_{index}'] = email
            self.response_list.append(return_obj)


def lambda_handler(event, context):
    input_document_path = '/home/matheus/Documents/work/api-taxreturns/src/TaxReturns/Data/data_file.xlsx'
    output_document_path = '/home/matheus/Documents/work/api-taxreturns/src/TaxReturns/Output/base_1.xlsx'

    print("Initializing...")
    facade = Facade()
    print("Processing...")
    facade.__post_init__(input_document_path)
    facade.process()
    print("Making PDFs...")
    facade.make_pdfs()
    print('Making xlsx file...')
    df = pd.DataFrame.from_dict(facade.response_list)
    df.to_excel(output_document_path)

    return {
        'statusCode': 200,
        'body': 'Lambda execution completed successfully.'
    }
