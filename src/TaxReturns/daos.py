import json
import requests as re

AZT_API_TOKEN='QVotQVBJS0VZOjZCRjRDNDg5LTFCREEtNDc3QS05MTA4LTNGRUY0NUZCRTU4OQ=='

class AztronicDao:
    def get_data(self, id, operation):
        payload = {"idContract": id, "action": operation, "env": "dev"}
        return re.post(
            'https://0qilw2i5ub.execute-api.us-east-1.amazonaws.com/default',
            data=json.dumps(payload)
        ).json()

    def get_ir(self, uuid):
        print(uuid)
        # header = {
        #     'Authorization': f'Basic {AZT_API_TOKEN}',
        #     'Content-Type': 'application/json'
        # }
        # endpoint = f'https://srv1.aztronic.com.br/az/apicollect/api/cliente/GetInformeIR/{uuid}/2022'
        # print(re.get(endpoint, headers=header))
        #
        # return re.get(endpoint, headers=header).json()

    def get_client(self, cpf_cnpj):
        header = {
            'Authorization': f'Basic {AZT_API_TOKEN}',
            'Content-Type': 'application/json'
        }
        endpoint = f'https://srv1.aztronic.com.br/az/apicollect/api/cliente/GetCliente/{cpf_cnpj}'
        return re.get(endpoint, headers=header).json()

    def get_client_email(self, cnpj_cpf):
        email = self.get_client(cnpj_cpf)
        return email['cliente']['email']

class TaxReturnDao:
    def create(self):
        pass

if __name__ == '__main__':
    x = AztronicDao().get_ir(129246)
    print(x)
