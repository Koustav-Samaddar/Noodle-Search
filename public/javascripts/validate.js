
function validateSearch() {
  const isEmpty = (/^\s*$/).test(document.getElementsByClassName('searchfield')[0].value);
  if (!isEmpty) {
    document.getElementById('loader').removeAttribute('hidden');
  };
  return !isEmpty;
};

function onSearchPageLoad() {
  document.getElementById('loader').setAttribute('hidden', '');
}

onSearchPageLoad();