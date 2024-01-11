import json

import requests as re

from helpers.gql_client import GqlClient

AZT_API_TOKEN = 'QVotQVBJS0VZOjZCRjRDNDg5LTFCREEtNDc3QS05MTA4LTNGRUY0NUZCRTU4OQ=='


class AztronicDao:
    def get_data(self, id, operation):
        payload = {"idContract": id, "action": operation, "env": "dev"}
        return re.post('https://0qilw2i5ub.execute-api.us-east-1.amazonaws.com/default',
            data=json.dumps(payload)).json()

    def get_ir(self, uuid):
        print(uuid)
        header = {'Authorization': f'Basic {AZT_API_TOKEN}', 'Content-Type': 'application/json'}
        endpoint = f'https://srv1.aztronic.com.br/az/apicollect/api/cliente/GetInformeIR/{uuid}/2022'
        print(re.get(endpoint, headers=header))

        return re.get(endpoint, headers=header).json()

    def get_client(self, cpf_cnpj):
        header = {'Authorization': f'Basic {AZT_API_TOKEN}', 'Content-Type': 'application/json'}
        endpoint = f'https://srv1.aztronic.com.br/az/apicollect/api/cliente/GetCliente/{cpf_cnpj}'
        return re.get(endpoint, headers=header).json()

    def get_client_email(self, cnpj_cpf):
        email = self.get_client(cnpj_cpf)
        return email['cliente']['email']


class TaxReturnDao:
    def __init__(self):
        self.contractId = ""

    def createContract(self, current_pdf_info):
        mutation = """
        mutation createContract(
          $unit: String,
          $email: String,
          $development: String,
          $date: String,
          $contractNumber: Int,
          $baseYear: String,
          $block: String,
          $balance: Float
        ) {
          createContractInfo(
            input: {
              unit: $unit,
              email: $email,
              development: $development,
              date: $date,
              contractNumber: $contractNumber,
              baseYear: $baseYear,
              block: $block,
              balance: $balance
            }
          ) {
            id
          }
        }
        """

        contract_info = current_pdf_info.get('contractInfo', {})
        gql = GqlClient()

        response = gql.post(mutation, {
            'unit': contract_info.get('unit', ""),
            'email': contract_info.get('email', ""),
            'development': contract_info.get('development', ""),
            'date': contract_info.get('date', ""),
            'contractNumber': contract_info.get('contractNumber', 0),
            'baseYear': contract_info.get('baseYear', ""),
            'block': contract_info.get('block', ""),
            'balance': contract_info.get('balance', 0.0),
        })

        data = response.json()
        self.contractId = data.get('createContractInfo', {}).get('id', None)

        return data

    def createInstallments(self, current_pdf_info):
        # Construct the mutation string with parameters
        contractId = "915cdf7d-ab26-4110-b627-cabbdffa671a"

        mutation = """
        mutation MyMutation(
          $amountPayed: Float,
          $creditDate: String,
          $payedInstallment: String
        ) {
          createInstallments(
            input: {
              amountPayed: $amountPayed,
              creditDate: $creditDate,
              payedInstallment: $payedInstallment
            }
          )
        }
        """
        gql = GqlClient()

        for installment_data in current_pdf_info.get('installments', []):
            response = gql.post(mutation, {
                'amountPayed': installment_data.get('amoutPayed', 0.0),  # Assuming a typo in 'amoutPayed'
                'contractinfoID': contractId,
                'creditDate': installment_data.get('creditDate', ""),
                'payedInstallment': installment_data.get('payedInstallment', ""),
            })

            data = response.json()
            print(data)

        return "Installments created successfully"  # Modify this as needed


if __name__ == '__main__':
    # x = AztronicDao().get_ir(129246)
    payload = {'installments': [{'creditDate': '1/2022', 'payedInstallment': '1 - Mensal', 'amoutPayed': 'R$ 0,00'},
                                {'creditDate': '2/2022', 'payedInstallment': '2 - Mensal', 'amoutPayed': 'R$ 0,00'},
                                {'creditDate': '3/2022', 'payedInstallment': '3 - Mensal', 'amoutPayed': 'R$ 0,00'},
                                {'creditDate': '4/2022', 'payedInstallment': '4 - Mensal', 'amoutPayed': 'R$ 0,00'},
                                {'creditDate': '5/2022', 'payedInstallment': '5 - Mensal', 'amoutPayed': 'R$ 0,00'},
                                {'creditDate': '6/2022', 'payedInstallment': '6 - Mensal', 'amoutPayed': 'R$ 0,00'},
                                {'creditDate': '7/2022', 'payedInstallment': '7 - Mensal', 'amoutPayed': 'R$ 0,00'},
                                {'creditDate': '8/2022', 'payedInstallment': '8 - Mensal', 'amoutPayed': 'R$ 0,00'},
                                {'creditDate': '9/2022', 'payedInstallment': '9 - Mensal', 'amoutPayed': 'R$ 0,00'},
                                {'creditDate': '10/2022', 'payedInstallment': '10 - Mensal', 'amoutPayed': 'R$ 0,00'},
                                {'creditDate': '11/2022', 'payedInstallment': '11 - Mensal', 'amoutPayed': 'R$ 0,00'},
                                {'creditDate': '12/2022', 'payedInstallment': '12 - Mensal', 'amoutPayed': 'R$ 0,00'}],
               'participants': [
                   {'name': 'AGOSTINHO FRANCISCO DE SOUZA', 'documentNumber': '011.615.038-62', 'participation': 100.0,
                    'email': 'consultor.agostinho@gmail.com'},
                   {'name': 'MARIETE DIEGUES DE SOUZA', 'documentNumber': '040.429.738-25', 'participation': 0.0,
                    'email': 'consultor.agostinho@gmail.com'}],
               'contractInfo': {'development': 'PONTTE - HOME EQUITY', 'contractNumber': 130274, 'baseYear': '2022',
                                'block': 'ÚNICO', 'unit': '302', 'date': '06/06/2022', 'email': 'lucas@pontte.com.br',
                                'balance': 0.0, 'saldo': 'R$ 0,00'},
               'receiverInfo': {'receiver': 'MAUÁ CAPITAL REAL ESTATE DEBT III \n FUNDO DE INVESTIMENTO MULTIMERCADO',
                                'cnpj': '30.982.547/0001-09',
                                'address': 'Av. Brg. Faria Lima, 1485 - 18º andar - Pinheiros, São Paulo - SP, 01452-002',
                                'date': 'SÃO PAULO, 05 DE FEVEREIRO DE 2023'}}
    # x = TaxReturnDao().createContract(payload)
    z = TaxReturnDao().createInstallments(payload)

    print(z)
