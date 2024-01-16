import logging
from dataclasses import dataclass

from client import GqlClient
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


from dataclasses import dataclass


@dataclass
class ParticipantInfo:
    name: str
    email: str
    documentNumber: str
    participationPercentage: float


@dataclass
class ContractInfoDao:
    gql_client: GqlClient

    def create_contract_info(self, contract_info: ContractInfo):
        variables = {
            "balance": contract_info.balance,
            "block": contract_info.block,
            "base_year": contract_info.base_year,
            "contract_number": contract_info.contract_number,
            "date": contract_info.date,
            "development": contract_info.development,
            "email": contract_info.email,
            "unit": contract_info.unit,
        }

        try:
            result = self.gql_client.post(gql_mutation_create_contract, variables)
            return result.get("createContractInfo")
        except Exception as e:
            logging.error(f"Failed to create contract: {str(e)}")
            return None


@dataclass
class ParticipantsDao:
    gql_client: GqlClient

    def create_participant(self, name, email, documentNumber, participationPercentage, contract_info_id):
        variables = {
            "name": name,
            "email": email,
            "documentNumber": documentNumber,
            "participation_percentage": participationPercentage,
            "contract_info_id": contract_info_id,
        }

        try:
            result = self.gql_client.post(gql_mutation_create_participant, variables)
            return result.get("createParticipants")
        except Exception as e:
            logging.error(f"Failed to create participant: {str(e)}")
            return None


@dataclass
class InstallmentInfo:
    amountPayed: float
    creditDate: str
    payedInstallment: str
    contractinfoID: str


@dataclass
class InstallmentsDao:
    gql_client: GqlClient

    def create_installment(self, installment_info: InstallmentInfo) -> dict:
        variables = installment_info.__dict__
        try:
            result = self.gql_client.post(gql_mutation_create_installment, variables)
            return result.get("createInstallments", {})
        except Exception as e:
            logging.error(f"Failed to create installment: {str(e)}")
            return {}


@dataclass
class TaxReturnsFacade:
    gql_client: GqlClient
    contract_id: str = None  # Initialize contract_id to None

    def create_contract_info(self, contract_info: ContractInfo):
        contract_info_dao = ContractInfoDao(self.gql_client)
        contract_result = contract_info_dao.create_contract_info(contract_info)

        if contract_result:
            logging.info(f"Contract created: {contract_result['id']}")
            return contract_result['id']
        else:
            logging.error("Contract creation failed.")
            return None

    def create_participants(self, participants_data: list, contract_info_id: str):
        participants_dao = ParticipantsDao(self.gql_client)

        for participant_data in participants_data:
            created_participant = participants_dao.create_participant(
                name=participant_data["name"],
                email=participant_data["email"],
                documentNumber=participant_data["documentNumber"],
                participationPercentage=participant_data["participationPercentage"],
                contract_info_id=contract_info_id,
            )

            if created_participant:
                logging.info(f"Participant created: {created_participant['id']}")
            else:
                logging.error("Participant creation failed.")

    def create_installments(self, installments_data: list, contract_info_id: str):
        if not self.contract_id:
            logging.error("Contract ID is not available. Cannot create installments.")
            return

        installments_dao = InstallmentsDao(self.gql_client)

        for installment_data in installments_data:
            installment_info = InstallmentInfo(**installment_data)
            installment_info.contractinfoID = contract_info_id  # Set contract info ID
            created_installment = installments_dao.create_installment(installment_info)

            if created_installment:
                logging.info(f"Installment created: {created_installment.get('id')}")
            else:
                logging.error("Installment creation failed.")

    def create_contract_info_with_participants_and_with_installments(self, event):
        # Create contract info
        contract_info = ContractInfo(
            balance=event["balance"],
            block=event["block"],
            base_year=event["baseYear"],
            contract_number=event["contractNumber"],
            date=event["date"],
            development=event["development"],
            email=event["email"],
            unit=event["unit"],
        )

        contract_info_id = self.create_contract_info(contract_info)

        if contract_info_id:
            # Set the contract ID
            self.contract_id = contract_info_id

            # Extract participants and create participants
            participants_data = event.get("Participants", [])
            self.create_participants(participants_data, contract_info_id)

            # Extract installments and create installments
            installments_data = event.get("Installments", [])
            self.create_installments(installments_data, contract_info_id)


if __name__ == "__main__":
    event = {
        "balance": 0,
        "baseYear": "2022",
        "block": "H",
        "contractNumber": 129238,
        "date": "04/07/2019",
        "development": "PONTTE - HOME EQUITY",
        "email": "lucas@pontte.com.br",
        "unit": "10",
        "Participants": [
            {
                "documentNumber": "05632835804",
                "email": "lucas@pontte.com.br",
                "name": "CLAUDIA LUCAS DOS REIS",
                "participationPercentage": 50
            },
            {
                "documentNumber": "00598551859",
                "email": "lucas@pontte.com.br",
                "name": "LAERCIO LUCAS DOS REIS",
                "participationPercentage": 50
            }
        ],
        "Installments": [
            {
                "amountPayed": 1000.0,
                "creditDate": "01/01/2023",
                "payedInstallment": "Installment 1",
                "contractinfoID": "your_contract_info_id_here"  # Add the contract info ID here
            },
            {
                "amountPayed": 800.0,
                "creditDate": "02/01/2023",
                "payedInstallment": "Installment 2",
                "contractinfoID": "your_contract_info_id_here"  # Add the contract info ID here
            }
        ]
    }

    # Create a GqlClient instance
    gql_client = GqlClient()

    # Initialize TaxReturnsFacade with the GqlClient
    tax_returns_facade = TaxReturnsFacade(gql_client=gql_client)
    tax_returns_facade.create_contract_info_with_participants_and_with_installments(event)
