const { getNowShortDateString } = require('./helpers/date');
const { logoPontteSVG } = require('./assets/svg');

const header = (page, part, stacks) => {
  let header = '';

  stacks.forEach((stack, index) => {
    const pageNumbers = stack.positions.map(position => [position.pageNumber, index]);
    const currentPage = pageNumbers.find(number => number[0] === page);
    if (currentPage) header = part[currentPage[1]].name;
  });

  return [
    {
      columns: [
        {
          svg: logoPontteSVG,
          width: 140
        },
        {
          stack: [
            { text: header, bold: true, fontSize: 8 },
            { text: `ANO BASE 2022`, fontSize: 8 }
          ],
          alignment: 'right',
          margin: [0, 5, 0, 0]
        }
      ],
      margin: [40, 30, 40, 0]
    }
  ];
};

const footer = (currentPage, pageCount) => ({
  text: { text: `${currentPage.toString()} de ${pageCount}`, fontSize: 10 },
  alignment: 'right',
  margin: [40, 30, 40, 0]
});

module.exports = { footer, header };
