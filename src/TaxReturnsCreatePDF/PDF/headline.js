const {
  ColorScheme: { $MAIN_DARK, $MAIN_PURPLE }
} = require('./constants');
const text = ({ text, props }) => {
  return text ? { text, ...props } : {};
};

const createHeadline = (title, subtitle = '') => ({
  stack: [
    {
      columns: [
        text({ text: `${title}\n\n`, props: { fontSize: 12, bold: true, color: $MAIN_PURPLE} }),
      ]
    },
    {
      text: subtitle,
      margin: [0, 2, 0, 0], 
      fontSize: 12,
      bold: true,
      color: $MAIN_PURPLE
    },
    {
      canvas: [
        {
          type: 'rect',
          x: 0,
          y: 5,
          w: 522,
          h: 2,
          r: 0,
          color: $MAIN_DARK
        }
      ]
    }
  ],
  pageBreak: 'before',
  margin: [0, 20, 0, 20]
});

module.exports = { createHeadline, text };
