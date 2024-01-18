const axios = require('axios');

const getContractInfo = async (id) => {
  const query = `query MyQuery($id: ID!) {
    getContractInfo(id: $id) {
      total
      email
      development
      date
      contractNumber
      block
      baseYear
      balance
      Participants {
        items {
          contractinfoID
          documentNumber
          id
          email
          name
          participationPercentage
        }
      }
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
    }
}`;

  const variables = { id };

  const requestBody = {
    query,
    variables,
  };

  const config = {
    headers: {
      'x-api-key': 'da2-2ystthtjuvd5nhwu47qecm3ekm',
    },
  };

  try {
    const response = await axios.post('https://nce2nzequnem3jijcrgturt4oe.appsync-api.us-east-1.amazonaws.com/graphql', requestBody, config);

    return response.data;
  } catch (error) {
    throw error;
  }
};

module.exports = {
  getContractInfo,
};
