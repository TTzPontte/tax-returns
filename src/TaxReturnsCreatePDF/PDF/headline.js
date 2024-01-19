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
        text({ text: title, props: { fontSize: 12, bold: true, color: $MAIN_PURPLE} }),
        text({
          text: subtitle,
          props: { fontSize: 9, bold: true, alignment: 'right' }
        })
      ]
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

module.exports = { createHeadline };
