$(document).ready(() => {
  $("#state").select2({
    placeholder: "state",
    allowClear: true,
    width: "style",
  });
  $("#select2-state-container").siblings()[0].lastChild.id = "states";
});
