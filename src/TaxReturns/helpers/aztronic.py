# %%
import json
import boto3

ssm = boto3.client('ssm')
parameter = ssm.get_parameter(Name='/aztronic/apikey', WithDecryption=True)
print(parameter['Parameter']['Value'])

azt_api_key = parameter['Parameter']['Value']

import requests as re
def get_data(id, operation):
    payload = {"idContract": id, "action": operation, "env": "dev"}
    return re.post(
        'https://0qilw2i5ub.execute-api.us-east-1.amazonaws.com/default',
        data=json.dumps(payload)
    ).json()


def get_ir(uuid):
    header = {
        'Authorization': f'Basic {azt_api_key}',
        'Content-Type': 'application/json'
    }
    endpoint = f'https://srv1.aztronic.com.br/az/apicollect/api/cliente/GetInformeIR/{uuid}/2022'
    return re.get(endpoint, headers=header).json()


def get_client(cpf_cnpj):
    header = {
        'Authorization': f'Basic {azt_api_key}',
        'Content-Type': 'application/json'
    }
    endpoint = f'https://srv1.aztronic.com.br/az/apicollect/api/cliente/GetCliente/{cpf_cnpj}'
    return re.get(endpoint, headers=header).json()
