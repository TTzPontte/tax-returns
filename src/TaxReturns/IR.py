# ./src/IR.py
from dataclasses import dataclass, field
from typing import List, Optional

from dateutil.parser import parse as parse_date
from layers.common import format_br_doc, get_client_email


@dataclass
class Participante:
    cnpj_cpf: str
    nome: str
    participacao: float

    def __post_init__(self):
        self.email = get_client_email(self.cnpj_cpf)
        self.cnpj_cpf = format_br_doc(self.cnpj_cpf)

    def to_json(self):
        return {
            "name": self.nome,
            "documentNumber": self.cnpj_cpf,
            "participation": self.participacao,
            "email": self.email
        }


@dataclass
class Pagamento:
    mes: int
    valor_pago: float

    def __post_init__(self):
        if self.mes > 1:
            self.valor_pago = 0.0

    def to_json(self):
        return {
            'creditDate': f'{self.mes}/2022',
            'payedInstallment': f"{self.mes} - Mensal",
            'amountPayed': self.valor_pago,
        }


@dataclass
class Informeiro:
    empresa: str
    cnpj_cpf: str
    dt_contrato: str
    saldo: float
    participantes: List[Participante]
    pagamentos: List[Pagamento]


@dataclass
class IR:
    data: Informeiro
    contract_info: dict
    receiver_info: dict
    installments: Optional[list] = field(default_factory=list)
    participants: Optional[list] = field(default_factory=list)
    emails: Optional[list] = field(default_factory=list)

    def make_participants(self):
        participants = []
        for participant in self.data.participantes:
            self.emails.append(participant.email)
            participants.append(participant.to_json())
        return participants


    def to_json(self):
        it = [installment.to_json() for installment in self.data.pagamentos][0]['amountPayed']
        self.data.saldo = it
        self.saldo = it
        self.contract_info['saldo'] = it
        return {
            "installments": [installment.to_json() for installment in self.data.pagamentos],
            "participants": self.make_participants(),
            "contractInfo": self.contract_info,
            "receiverInfo": self.receiver_info
        }


def parse_json(data: dict) -> IR:
    informeiro_data = data['informeir']['informeir']
    contrato = data['contrato']

    participantes = [Participante(**participante) for participante in informeiro_data['participantes']]
    pagamentos = [Pagamento(**pagamento) for pagamento in informeiro_data['pagamentos']]
    saldo = pagamentos[0].valor_pago

    ir_info = Informeiro(
        empresa=informeiro_data['empresa'],
        cnpj_cpf=informeiro_data['cnpj_empresa'],
        dt_contrato=informeiro_data['dt_contrato'],
        saldo=saldo,
        participantes=participantes,
        pagamentos=pagamentos
    )

    contract_info = {
        'development': contrato['empreendimento'],
        'contractNumber': contrato['id_contrato'],
        'baseYear': '2022',
        'block': contrato['bloco'],
        'unit': contrato['unidade'],
        'date': parse_date(contrato['data_contrato']).strftime("%d/%m/%Y"),
        'email': 'lucas@pontte.com.br',
        'balance': saldo
    }
    _obj = {
        "data": ir_info,
        "contract_info": contract_info,
        "receiver_info": {
            "receiver": "MAUÁ CAPITAL REAL ESTATE DEBT III \n FUNDO DE INVESTIMENTO MULTIMERCADO",
            "cnpj": "30.982.547/0001-09",
            "address": "Av. Brg. Faria Lima, 1485 - 18º andar - Pinheiros, São Paulo - SP, 01452-002",
            # todo check date
            "date": "SÃO PAULO, 05 DE FEVEREIRO DE 2023"
        }
    }
    return IR(**_obj)
