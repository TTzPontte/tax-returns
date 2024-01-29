import json
import boto3

from Models.client import GqlClient
from Models.dao import TaxReturnsFacade


def invoke_lambda_function(event):
    try:
        tax_return_id = event
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

