const MONTHS = {
  1: 'Janeiro',
  2: 'Fevereiro',
  3: 'Março',
  4: 'Abril',
  5: 'Maio',
  6: 'Junho',
  7: 'Julho',
  8: 'Agosto',
  9: 'Setembro',
  10: 'Outubro',
  11: 'Novembro',
  12: 'Dezembro'
};

const formatMonth = monthNumber => {
  if (Number(monthNumber) === 0 || Number(monthNumber) === -1) return 'Nenhum';

  if (!monthNumber || monthNumber > 12) return '-';

  return MONTHS[monthNumber];
};

const getShortMonth = month => {
  return MONTHS[month].slice(0, 3);
};

const getNowShortDateString = () => {
  const newDate = new Date();
  const month = getShortMonth(newDate.getMonth() + 1);

  return `${newDate.getDate()} ${month} ${newDate.getFullYear()}`;
};

const formatDate = date => (date ? date.replace(/(\d{4})-(\d{2})-(\d{2})/, '$3/$2/$1') : '');

const getMonthYear = (dt, short = false) => {
  const date = new Date(dt);
  const month = date.getMonth() + 1;
  const year = date.getFullYear();
  const monthStr = short ? getShortMonth(month) : MONTHS[month];

  return `${monthStr} ${year}`;
};

const brDateToGlobal = date =>
  date
    .split('/')
    .reverse()
    .join('-');

const globalDateToBr = date =>
  date
    .split('-')
    .reverse()
    .join('/');

module.exports = { MONTHS, formatMonth, formatDate, globalDateToBr, getNowShortDateString, getMonthYear, brDateToGlobal };
