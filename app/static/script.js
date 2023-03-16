// BOOTSTRAP TOOLTIP ACTIVATION
const tooltipTriggerList = $('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(
  (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
);

const $fsymRadios = $(".fsym-radio");
const $tsymRadios = $(".tsym-radio");
const $form = $("form");

$fsymRadios.on("change", changeSelects.bind(null, "fsym-"));
$tsymRadios.on("change", changeSelects.bind(null, "tsym-"));

function changeSelects(dir, evt) {
  target = evt.target;
  $(target.parentElement).attr("disabled", true);

  for (type of ["fiat", "crypto", "comm"]) {
    if (target.id.indexOf(type) != -1) break;
  }

  const collapses = [...$(`.${dir}collapse`)].map(
    (el) => new bootstrap.Collapse(el, { toggle: false })
  );

  for (collapse of collapses) {
    if (collapse._element.id.indexOf(type) != -1) collapse.show();
    else collapse.hide();
  }

  setTimeout(() => {
    $(target.parentElement).attr("disabled", false);
  }, 350);
}

$form.on("submit", (e) => {
  e.preventDefault();
  if (!$form[0].checkValidity()) {
    e.preventDefault();
    e.stopPropagation();
  }

  $form.addClass("was-validated");
});
