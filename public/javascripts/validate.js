
const validateSearch = function () {
  const isEmpty = (/^\s*$/).test(document.getElementsByClassName('searchfield')[0].value);
  return !isEmpty;
};
