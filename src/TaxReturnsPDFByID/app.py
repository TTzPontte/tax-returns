import json
import boto3

from layers.common.Models.client import GqlClient
from layers.common.Models.dao import AppSyncDao


def invoke_lambda_function(event):
    try:
        tax_return_id = event['pathParameters']['taxReturnId']
        lambda_client = boto3.client('lambda')
        gql_client = GqlClient()
        dao = AppSyncDao(gql_client)
        contract_id = tax_return_id

        result = dao.get_record_by_contract_id(contract_id)
        payload_data = {'data': result}

        invocation_response = lambda_client.invoke(
            FunctionName='TaxReturnGeneratePDF-dev',
            InvocationType='RequestResponse',
            Payload=json.dumps(payload_data),
        )

        response_payload = json.loads(invocation_response['Payload'].read().decode('utf-8'))

        return response_payload

    except Exception as e:
        return str(e)

if __name__ == '__main__':
    sample_event = {
        'pathParameters': {
            'taxReturnId': '07ad7127-761a-4460-b515-40a15b09a61a'  # Substitua pelo ID desejado
        }
    }

    # Invoca a função lambda
    result = invoke_lambda_function(sample_event)
    print(result)
