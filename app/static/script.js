// BOOTSTRAP TOOLTIP ACTIVATION
const tooltipTriggerList = $('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(
  (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
);

const $form = $("form");

$form.on("submit", (e) => {
  e.preventDefault();
  if (!$form[0].checkValidity()) {
    e.preventDefault();
    e.stopPropagation();
  }

  $form.addClass("was-validated");
});
