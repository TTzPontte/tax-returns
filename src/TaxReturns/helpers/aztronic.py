# %%
import json

import requests as re
AZT_API_TOKEN='QVotQVBJS0VZOjZCRjRDNDg5LTFCREEtNDc3QS05MTA4LTNGRUY0NUZCRTU4OQ=='
def get_data(id, operation):
    payload = {"idContract": id, "action": operation, "env": "dev"}
    return re.post(
        'https://0qilw2i5ub.execute-api.us-east-1.amazonaws.com/default',
        data=json.dumps(payload)
    ).json()


def get_ir(uuid):
    header = {
        'Authorization': f'Basic {AZT_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    endpoint = f'https://srv1.aztronic.com.br/az/apicollect/api/cliente/GetInformeIR/{uuid}/2022'
    return re.get(endpoint, headers=header).json()


def get_client(cpf_cnpj):
    header = {
        'Authorization': f'Basic {AZT_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    endpoint = f'https://srv1.aztronic.com.br/az/apicollect/api/cliente/GetCliente/{cpf_cnpj}'
    return re.get(endpoint, headers=header).json()
