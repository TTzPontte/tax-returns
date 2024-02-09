const { getNowShortDateString } = require('./helpers/date');
const { logoPontteSVG } = require('./assets/svg');
const {
  ColorScheme: { $MAIN_PURPLE }
} = require('./constants');

const header = (page, part, stacks, previousIndex) => {
  let header = '';
  let yearBase = 'ANO BASE 2023'
  stacks.forEach((stack, index) => {
    const pageNumbers = stack.positions.map(position => [position.pageNumber, index]);
    const currentPage = pageNumbers.find(number => number[0] === page);
    
    if(currentPage){
      if(currentPage[1] > previousIndex){
        previousIndex = currentPage[1]
        header = part[currentPage[1]].name;
      }else{
       header = ''
       yearBase = ''
      }
    }
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
            { text: header, bold: true, fontSize: 14, color: $MAIN_PURPLE},
            { text: yearBase, fontSize: 10, color: $MAIN_PURPLE }
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
