import logging

# Configure logging at the beginning of the script
logging.basicConfig(level=logging.INFO)

# Define GraphQL Mutations for Contract, Participant, and Installment (unchanged)

gql_query_get_contractInfo = """
  query getContractInfo($id: ID!) {
  getContractInfo(id: $id) {
    total
    email
    development
    date
    contractNumber
    block
    baseYear
    balance
    Installments {
      items {
        payedInstallment
        id
        creditDate
        createdAt
        contractinfoID
        amountPayed
      }
    }
    unit
    Participants {
      items {
        name
        participationPercentage
        email
        documentNumber
      }
    }
  }
}
"""

gql_query_get_participants_by_document_number = """
query GetParticipantsByDocumentNumber($documentNumber: String!) {
  listParticipants(filter: { documentNumber: { eq: $documentNumber } }) {
    items {
      documentNumber
      email
      id
      contractinfoID
    }
  }
}
"""

gql_mutation_create_contract = """
    mutation CreateContract(
        $balance: Float!,
        $block: String!,
        $base_year: String!,
        $contract_number: Int!,
        $date: String!,
        $development: String!,
        $email: String!,
        $unit: String!
    ) {
        createContractInfo(
            input: {
                balance: $balance,
                baseYear: $base_year,
                block: $block,
                contractNumber: $contract_number,
                date: $date,
                development: $development,
                email: $email,
                unit: $unit
            }
        ) {
            id
            email
            createdAt
            _version
        }
    }
"""

gql_mutation_create_participant = """
    mutation CreateParticipant(
        $name: String!,
        $email: String!,
        $documentNumber: String,
        $participation_percentage: Float,
        $contract_info_id: ID!
    ) {
        createParticipants(input: {
            name: $name,
            email: $email,
            documentNumber: $documentNumber,
            participationPercentage: $participation_percentage,
            contractinfoID: $contract_info_id
        }) {
            id
            name
            email
            documentNumber
            participationPercentage
        }
    }
"""

gql_mutation_create_installment = """
    mutation CreateInstallment(
        $amountPayed: Float!,
        $creditDate: String!,
        $payedInstallment: String,
        $contractinfoID: ID!
    ) {
        createInstallments(input: {
            amountPayed: $amountPayed,
            creditDate: $creditDate,
            payedInstallment: $payedInstallment,
            contractinfoID: $contractinfoID
        }) {
            id
            amountPayed
            creditDate
            payedInstallment
        }
    }
"""
