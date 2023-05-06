const $fsymRadios = $("input[name=fsym-radio]");
const $tsymRadios = $("input[name=tsym-radio]");
const $form = $("form");

$fsymRadios.on("change", changeSelects.bind(null, "fsym-"));
$tsymRadios.on("change", changeSelects.bind(null, "tsym-"));

function changeSelects(dir, evt) {
  // Get radio that was clicked
  radio = $(evt.target);
  // Disable all radios of that direction
  radio.parent().attr("disabled", true);
  setTimeout(() => {
    // re-enable once animation over
    radio.parent().attr("disabled", false);
  }, 350);

  // Get collapse to show from data tag
  targetId = radio.data("target-collapse");

  const collapses = [...$(`.${dir}collapse`)].map(
    (el) => new bootstrap.Collapse(el, { toggle: false })
  );
  for (collapse of collapses) {
    if (collapse._element.id === targetId) collapse.show();
    else collapse.hide();
  }
}
