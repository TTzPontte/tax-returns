const formatMoney = (value = 0) =>
  value
    ? `R$ ${Number(value)
        .toFixed(2)
        .replace('.', ',')
        .replace(/\d(?=(\d{3})+,)/g, '$&.')}`
    : 'R$ 0,00';

const formatPercentage = (value) => {
  const formattedValue = Number(value).toFixed(2).replace('.', ',');
  return formattedValue === '0,00' ? "0%" : `${formattedValue}%`;
};

const removeFormatMoney = value => (typeof value !== 'string' ? value : parseFloat(value.replace(/[R$ .]/g, '').replace(',', '.')));

const formatMoneyWOCurrency = value =>
  value
    ? `${Number(value)
        .toFixed(2)
        .replace('.', ',')
        .replace(/\d(?=(\d{3})+,)/g, '$&.')}`
    : '0,00';


const formatCpfCnpj = (value) => {
  const cleanValue = value.replace(/[^\d]/g, ''); 
  if (cleanValue.length === 11) { // CPF
    return cleanValue.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
  } else if (cleanValue.length === 14) { // CNPJ
    return cleanValue.replace(/(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})/, '$1.$2.$3/$4-$5');
  }
};


module.exports = { formatPercentage, removeFormatMoney, formatMoneyWOCurrency, formatMoney, formatCpfCnpj };
