const {
  ColorScheme: { $MAIN_PURPLE }
} = require('../../constants');

const buildHeaderRow = (list, margin = [0, 60, 0, 0]) => ({
  columns: list.map(({ title, value }) => ({
    width: 140,
    stack: [
      {
        columns: [
          {
            width: '*',
            stack: [
              { text: title, fontSize: 8 },
              {
                text: value,
                bold: true,
                fontSize: 13,
                color: $MAIN_PURPLE
              }
            ]
          }
        ]
      }
    ],
    columnGap: 10
  })),
  columnGap: 15,
  margin
});

const HeaderTitle = () => ({
  text: `Demonstrativo de Valores Pagos`,
  fontSize: 24,
  bold: true
});

const IntroductionPage = ({ contractInfo }) => {
  const buildHeaderList = list => list.map(i => ({ title: i, value: contractInfo[i] }));
  contractInfo['DATA DO CONTRATO'] = contractInfo['DATA']; // @TODO TechDEBT: A LITTLE DIRTY HACK DUE IR 2023 TIME

  const row2 = buildHeaderList(['BLOCO', 'UNIDADE', 'DATA DO CONTRATO']);
  const row1 = buildHeaderList(['EMPREENDIMENTO', 'CONTRATO', 'ANO BASE']);
  const buildHeader = () => [buildHeaderRow(row1), buildHeaderRow(row2)];

  return {
    columns: [
      {
        width: 4,
        canvas: [
          {
            type: 'rect',
            x: 0,
            y: 0,
            w: 4,
            h: 260,
            r: 5,
            color: $MAIN_PURPLE,
            lineColor: $MAIN_PURPLE
          }
        ]
      },
      {
        width: '*',
        stack: [HeaderTitle(), ...buildHeader()]
      }
    ],
    margin: [45, 30, 0, 0],
    columnGap: 20
  };
};

module.exports = { IntroductionPage };
