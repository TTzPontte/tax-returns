const formatMoney = (value = 0) =>
  value
    ? `R$ ${Number(value)
        .toFixed(2)
        .replace(".", ",")
        .replace(/\d(?=(\d{3})+,)/g, "$&.")}`
    : "R$ 0,00";

const formatPercentage = (value) => {
  const formattedValue = Number(value).toFixed(2).replace(".", ",");
  return formattedValue === "0,00" ? "0%" : `${formattedValue}%`;
};

const removeFormatMoney = (value) =>
  typeof value !== "string"
    ? value
    : parseFloat(value.replace(/[R$ .]/g, "").replace(",", "."));

const formatMoneyWOCurrency = (value) =>
  value
    ? `${Number(value)
        .toFixed(2)
        .replace(".", ",")
        .replace(/\d(?=(\d{3})+,)/g, "$&.")}`
    : "0,00";

module.exports = {
  formatPercentage,
  removeFormatMoney,
  formatMoneyWOCurrency,
  formatMoney,
};
