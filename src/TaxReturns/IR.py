# ./src/IR.py
from dataclasses import dataclass, field
from typing import List, Optional

from dateutil.parser import parse as parse_date

from helpers.utils import format_br_doc, get_client_email


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


def parse_participante(participante_data: dict) -> Participante:
    return Participante(**participante_data)


def parse_pagamento(pagamento_data: dict) -> Pagamento:
    return Pagamento(**pagamento_data)


def parse_informeiro(informeiro_data: dict) -> Informeiro:
    participantes = [parse_participante(part) for part in informeiro_data.get('participantes', [])]
    pagamentos = [parse_pagamento(pay) for pay in informeiro_data.get('pagamentos', [])]
    saldo = pagamentos[0].valor_pago if pagamentos else 0

    return Informeiro(
        empresa=informeiro_data.get('empresa'),
        cnpj_cpf=informeiro_data.get('cnpj_empresa'),
        dt_contrato=informeiro_data.get('dt_contrato'),
        saldo=saldo,
        participantes=participantes,
        pagamentos=pagamentos
    )


def parse_contract_info(contrato: dict, saldo: float) -> dict:
    return {
        'development': contrato.get('empreendimento'),
        'contractNumber': contrato.get('id_contrato'),
        'baseYear': '2022',
        'block': contrato.get('bloco'),
        'unit': contrato.get('unidade'),
        'date': parse_date(contrato.get('data_contrato')).strftime("%d/%m/%Y"),
        'email': 'lucas@pontte.com.br',
        'balance': saldo
    }


def parse_json(informeir_data: dict, contrato: dict) -> IR:
    informeiro_data = informeir_data.get('informeir', {})

    ir_info = parse_informeiro(informeiro_data)
    contract_info = parse_contract_info(contrato, ir_info.saldo)

    _obj = {
        "data": ir_info,
        "contract_info": contract_info,
        "receiver_info": {
            "receiver": "MAUÁ CAPITAL REAL ESTATE DEBT III \n FUNDO DE INVESTIMENTO MULTIMERCADO",
            "cnpj": "30.982.547/0001-09",
            "address": "Av. Brg. Faria Lima, 1485 - 18º andar - Pinheiros, São Paulo - SP, 01452-002",
            "date": "SÃO PAULO, 05 DE FEVEREIRO DE 2023"
        }
    }

    return IR(**_obj)
