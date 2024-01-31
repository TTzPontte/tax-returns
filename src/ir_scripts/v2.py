import csv
import json
import logging
from dataclasses import dataclass

from common_layers.helpers.utils import parse_to_brl
from common_layers.helpers.base_dao import Dao

# Constants for JSON file paths
INFORMEIR_JSON_FILE = '/Users/Mr-i-me/code/Mr-i-me-pontte/ir/tax-returns/src/ir_scripts/data/output/_informeir_dict.json'
FINANCES_JSON_FILE = '/Users/Mr-i-me/code/Mr-i-me-pontte/ir/tax-returns/src/ir_scripts/data/output/_get_finances_list.json'

# Configure logging to a file named 'facade.log' with ERROR level
logging.basicConfig(filename='facade.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


@dataclass
class Pagamento:
    mes: int
    valor_pago: float

    def __post_init__(self):
        if self.mes > 1:
            self.valor_pago = 0.0

    def to_json(self):
        return {
            'creditDate': f'{self.mes}/2023',
            'payedInstallment': f"{self.mes} - Mensal",
            'amoutPayed': parse_to_brl(self.valor_pago)
        }


@dataclass
class Facade:
    informeir_file: str = INFORMEIR_JSON_FILE
    finances_file: str = FINANCES_JSON_FILE

    def __post_init__(self):
        # Load JSON data from files
        self.informeir_data = self.load_json(self.informeir_file)
        self.finances_data = self.load_json(self.finances_file)

        # Create instances of Dao for database access
        self.dao = Dao('Klavi-ClosedStatement-staging')
        self.dao2 = Dao('TaxReturnsDynamo-dev')
        self.dao3 = Dao('taxReturns_ir_list')

    def load_json(self, input_json_file):
        try:
            with open(input_json_file, 'r') as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Input JSON file '{input_json_file}' not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON format in '{input_json_file}'.")

    def scan_klavi(self):
        try:
            return self.dao.get_all()
        except Exception as e:
            logging.error(f"Error scanning Klavi database: {e}")
            return []

    def process_records(self):
        # Create a list to store installment data
        installments_list = []

        # Create a dictionary to store installments by contract_id
        installments_dict = {}

        # Fetch records from the database
        self.records = self.scan_klavi()

        # Iterate through records and process them
        self.saldo_dict = {}
        for record in self.records:
            id_ = record.get('id')
            ir_info = self.informeir_data.get(id_, {}).get('informeir', None)
            if ir_info is not None:
                saldo = ir_info.get('saldo')
                self.saldo_dict[id_] = saldo
                pagamentos = ir_info.get('pagamentos', [])

                # Process the ir_info and finance_info as needed
                for pagamento_data in pagamentos:
                    pagamento = Pagamento(pagamento_data.get('mes', 0), pagamento_data.get('valor_pago', 0.0))
                    installment_data = {
                        'contract_id': id_,
                        **pagamento.to_json()  # Include installment data
                    }
                    installments_list.append(installment_data)

                    # Add installment to dictionary by contract_id
                    installments_dict.setdefault(id_, []).append(pagamento.to_json())

        # Export data to CSV and JSON
        self.export_to_csv(installments_list, 'installments.xlsx')
        self.save_to_json(installments_dict, 'installments.json')

        # Create contracts by combining dao records and installments
        self.create_contracts(self.records, installments_dict)

    def export_to_csv(self, data, output_csv_file):
        try:
            with open(output_csv_file, 'w', newline='') as csv_file:
                fieldnames = ['contract_id', 'creditDate', 'payedInstallment', 'amoutPayed']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            print(f"CSV file '{output_csv_file}' has been created successfully.")
        except Exception as e:
            print(f"An error occurred while writing CSV file: {str(e)}")

    def save_to_json(self, data, output_json_file):
        try:
            with open(output_json_file, 'w') as json_output_file:
                json.dump(data, json_output_file, indent=4)
            print(f"JSON file '{output_json_file}' has been created successfully.")
        except Exception as e:
            print(f"An error occurred while writing JSON file: {str(e)}")

    def create_contracts(self, records, installments_dict):
        for record in records:
            id_ = record.get('id')
            # Combine the dao record and installments for each contract
            contract_data = {
                **record,
                'saldo': self.saldo_dict.get(id_),
                'installments': installments_dict.get(id_, [])
            }
            # Save the contract data to dao3
            self.dao3.create_item(contract_data)
            print(f"Contract created for ID {id_}")


if __name__ == '__main__':
    print("Initializing...")
    facade = Facade()  # Use default values for file paths and database name

    print("Processing records...")
    facade.process_records()
    print(f"Processed {len(facade.scan_klavi())} records.")
