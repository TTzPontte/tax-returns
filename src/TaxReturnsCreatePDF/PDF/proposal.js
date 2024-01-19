const { formatPercentage } = require('./helpers/number');
const {
  fillColor,
  ColorScheme: { $MAIN_PURPLE }
} = require('./constants');

const formatValue = value => ({ text: value, bold: true, fontSize: 10, color: $MAIN_PURPLE });

const layout = {
  defaultBorder: false,
  fillColor: rowIndex => fillColor(rowIndex),
  paddingLeft: () => 15
};

const receiverSection = ({
  receiver = 'MAUÁ CAPITAL REAL ESTATE DEBT III \n FUNDO DE INVESTIMENTO MULTIMERCADO',
  cnpj = '30.982.547/0001-09',
  address = 'Av. Brg. Faria Lima, 1485 - 18º andar - Pinheiros, São Paulo - SP',
  date = 'SÃO PAULO, 05 DE FEVEREIRO DE 2023'
}) => ({
  style: 'proposalTable',
  table: {
    headerRows: 0,
    widths: ['40%', '60%'],
    body: [
      ['FONTE RECEBEDORA', receiver],
      ['CNPJ', cnpj],
      ['ENDEREÇO', address],
    ]
  },
  layout,
  margin: [0, 20, 0, 0]
});
const participantsSection = ({ name = 'PADANIA CONSULTORIA EIRELI', documentNumber = '06.109.309/0001-09', participationPercentage = '0%' }) => ({
  style: 'proposalTable',
  table: {
    headerRows: 0,
    widths: ['40%', '60%'],
    body: [
      ['NOME/RAZÃO SOCIAL', name],
      ['CPF/CNPJ', documentNumber],
      ['PARTICIPAÇÃO', formatValue(formatPercentage(participationPercentage))]
    ]
  },
  layout,
  margin: [0, 40, 0, 0]
});

const proposal = ({ proposal: { participants, receiverInfo } }) => {
  const rowsParticipants = participants.map(participantsSection);
  const rowReceiverInfo = receiverSection(receiverInfo);

  return {
    columns: [
      {
        stack: [rowsParticipants, rowReceiverInfo],
        margin: [45, 30, 0, 0]
      }
    ]
  };
};

module.exports = { proposalPage: proposal };
