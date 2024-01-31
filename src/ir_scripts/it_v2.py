import json
import boto3
from decimal import Decimal

# Assuming new_list_data is a list of IDs
from Data.new_list import new_list_data


class Dao:
    def __init__(self, table_name):
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def get_all(self):
        items = []
        last_evaluated_key = None

        while True:
            params = {'ExclusiveStartKey': last_evaluated_key} if last_evaluated_key else {}
            response = self.table.scan(**params)
            scanned_items = response.get('Items', [])
            last_evaluated_key = response.get('LastEvaluatedKey', None)

            items.extend(scanned_items)

            if not last_evaluated_key:
                break

        return items


def load_json(input_json_file):
    try:
        with open(input_json_file, 'r') as json_file:
            return json.load(json_file)
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return {}


def build_installments(contract_ids, informeir_list):
    installments_data = []

    for contract_id in contract_ids:
        payments = informeir_list.get(str(contract_id), {}).get('informeir', {}).get('pagamentos', [])
        for payment in payments:
            installments_data.append({
                'contract_id': contract_id,
                'creditDate': f"{payment.get('mes')}/2022",
                'payedInstallment': f"{payment.get('mes')} - Mensal",
                'amountPayed': f"R${float(payment.get('valor_pago', 0)): .2f}"
            })

    return installments_data


def main():
    table_name = 'YourDynamoDBTableName'  # Replace with your DynamoDB table name
    input_json_file = 'Data/json_aztronic_responses/_informeir_list.json'

    dao = Dao(table_name)
    db_records = dao.get_all()
    contract_ids = [item['contract_id'] for item in db_records]  # Extract contract_id from each record

    informeir_list = load_json(input_json_file)
    installments_data = build_installments(contract_ids, informeir_list)

    # Optionally, you can print or save installments_data as needed
    print(installments_data)


if __name__ == "__main__":
    main()
