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
  const options = {
    alignment: "center",
    color: $MAIN_DARK,
  };

  const data = installments.map((installmentItem) => {
    if (installmentItem) {
      const { creditDate, payedInstallment, amountPayed } = installmentItem;
      return [
        { text: creditDate, ...options },
        { text: payedInstallment, ...options },
        { text: amountPayed, ...options },
      ];
    }
  });

  return data;
};

const totalFooter = ({ total }) => [
  { fillColor: $WHITE, text: "" },
  {
    fillColor: $GRAY_1,
    text: "Total",
    alignment: "center",
  },
  { fillColor: $GRAY_1, text: formatMoney(total), alignment: "center" },
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
  proposal: { installment: installments },
  contractInfo: { balance = "0,00", total = "0,00", name },
}) => ({
  stack: [
    createHeadline(
      `TITULAR: ${name}\n SALDO DEVEDOR EM 31/12/2023: ${balance}`
    ),
    installmentsTable({
      installments,
      total,
    }),
  ],
});
module.exports = { installmentsPage };
