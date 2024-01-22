import logging
from dataclasses import dataclass
from mutations import (
    gql_mutation_create_contract,
    gql_mutation_create_installment,
    gql_mutation_create_participant,
)

# Configure logging at the beginning of the script
logging.basicConfig(level=logging.INFO)


# Define data classes for better structure and readability
@dataclass
class ContractInfo:
    balance: float
    block: str
    base_year: str
    contract_number: int
    date: str
    development: str
    email: str
    unit: str


@dataclass
class InstallmentInfo:
    amountPayed: float
    creditDate: str
    payedInstallment: str
    contractinfoID: str
