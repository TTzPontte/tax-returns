const { createHeadline } = require("./headline");
const {
  ColorScheme: { $MAIN_DARK, $MAIN_PURPLE, $WHITE, $GRAY_1 },
  fillColor,
} = require("./constants");
const { formatMoney } = require("./helpers/number");

const layout = {
  paddingTop: (rowIndex) => (rowIndex > 0 ? 10 : 3),
  paddingBottom: (rowIndex) => (rowIndex > 0 ? 10 : 3),
  fillColor: (rowIndex) =>
    rowIndex === 0 ? $MAIN_PURPLE : fillColor(rowIndex),
  hLineColor: () => "white",
  vLineColor: () => "white",
  paddingLeft: () => 0,
  paddingRight: () => 0,
};

const creatHeader = (
  options = {
    alignment: "center",
    color: $WHITE,
    lineHeight: 0.5,
    fontSize: 10,
    bold: true
  },
  marginSingleLine = [0, 10, 0, 0]
) => [
  {
    text: "Data do Crédito",
    ...options,
    margin: marginSingleLine,
  },
  { text: "Parcela", ...options, margin: marginSingleLine },
  { text: "Valor Pago", ...options, margin: marginSingleLine },
];

const createRow = ({ installments = [] }) => {
  const sortedInstallments = installments.sort((a, b) => {
    const [monthA, yearA] = a.creditDate.split('/').map(Number);
    const [monthB, yearB] = b.creditDate.split('/').map(Number);

    if (yearA !== yearB) {
      return yearA - yearB;
    }

    return monthA - monthB;
  });

  const options = {
    alignment: "center",
    color: $MAIN_DARK,
    fontSize: 10
  };

  const data = sortedInstallments.map((installmentItem) => {
    if (installmentItem) {
      const { creditDate, payedInstallment, amountPayed } = installmentItem;

      const [month, year] = creditDate.split('/');
      const formattedCreditDate = `${month.padStart(2, '0')}/${year}`;

      return [
        { text: formattedCreditDate, ...options },
        { text: 'Entrada / Mensal / Intermediária / Final', ...options },
        { text: formatMoney(amountPayed), ...options },
      ];
    }
  });

  return data;
};

const totalFooter = ({ total }) => [
  { fillColor: $GRAY_1, text: "" },
  {
    fillColor: $GRAY_1,
    text: "Total",
    alignment: "center",
    bold: true,
    fontSize: 10
  },
  { fillColor: $GRAY_1, text: formatMoney(total), alignment: "center", bold: true, fontSize: 10},
];
const installmentsTable = ({ installments, total = "10000000,00000" }) => ({
  style: "proposalTable",
  table: {
    headerRows: 1,
    widths: [100, "*", 100],
    heights: [30],
    body: [
      creatHeader(),
      ...createRow({ installments }),
      totalFooter({ total }),
    ],
  },
  layout,
  margin: [0, 0, 0, 10],
  pageBreak: "after",
});

const installmentsPage = ({
  proposal: { installment: installments, participants },
  contractInfo: { balance = "0,00", total = "0,00", name = 'teste' },
}) => ({
  stack: [
    createHeadline(
      `TITULAR: ${participants[0].name}`, `SALDO DEVEDOR EM 31/12/2023: R$ ${parseInt(balance).toFixed(2)}` 
    ),
    installmentsTable({
      installments,
      total,
    }),
  ],
});
module.exports = { installmentsPage };
