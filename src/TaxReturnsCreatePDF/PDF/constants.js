class ColorScheme {
  constructor() {
    this.$MAIN_PURPLE = '#5C3B6B';
    this.$MAIN_DARK = '#3B3349';
    this.$WHITE = '#FFFFFF';
    this.$GRAY_1 = '#E8E8EF';
    this.$GRAY_2 = '#EEEEF2';
    this.$GRAY_3 = '#C3C3D5';
  }
}
const colors = new ColorScheme();
const fillColor = rowIndex => (rowIndex % 2 === 0 ? colors.$GRAY_1 : colors.$GRAY_2);

module.exports = { ColorScheme: colors, fillColor };
