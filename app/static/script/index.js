/** Moves results screen down if window too short, otherwise gets
 * set to window height (#first-screen height is 100vh) */
function repositionScreen2() {
  $("#second-screen").offset({ top: $("#first-screen").height() });
}
$(window).on("resize", repositionScreen2);
repositionScreen2();

$form.on("submit", handleForm);

async function handleForm(e) {
  e.preventDefault();

  // Bootstrap validation
  if (!$form[0].checkValidity()) {
    $form.addClass("was-validated");
    return;
  } else $form.removeClass("was-validated");

  // Disable submit button and show loading spinner
  $("#submit-button").attr("disabled", true);
  $("#submit-spinner").removeClass("d-none");

  // Find which type of currencies were chosen
  for (fromButton of $fsymRadios) if (fromButton.checked) break;
  for (toButton of $tsymRadios) if (toButton.checked) break;
  // From those, get the corresponding select
  const fromSelect = $($(fromButton).data("target-select"));
  const toSelect = $($(toButton).data("target-select"));

  // Get values from form
  const from_sym = fromSelect.val();
  const to_sym = toSelect.val();
  const amount = $("#amount").val();
  const date = $("#date").val();

  const resp = await axios.post(
    "/convert",
    (params = { from_sym, to_sym, amount, date })
  );

  // Re-enable submit and hide spinner
  $("#submit-button").attr("disabled", false);
  $("#submit-spinner").addClass("d-none");

  // If error was returned from ajax, show error message and stop
  if (resp.data.error) {
    toastList[0].show();
    return;
  }

  // Get data from response
  const btcEquiv = resp.data.btc_equiv;
  const btcPrice = resp.data.btc_price;
  // Also get current price from element in screen
  const currentBtcPrice = Number(
    $("#current-price").text().slice(16).replace(/,+/g, "")
  );

  // Get commodity name if needed
  if (to_sym.indexOf("com_" === 0)) {
    const commName = $(`#${toSelect[0].id} option:selected`).text();
    $("#to-sym").text(commName);
  } else $("#to-sym").text(to_sym);

  // Add data to result section
  $("#usd-result").text(formatPrice(btcEquiv * currentBtcPrice));
  $("#btc-result").text(formatPrice(btcEquiv));
  $("#btc-price").text(formatPrice(btcPrice, 2));

  // Show result section and scroll to it
  $("#second-screen").removeClass("d-none")[0].scrollIntoView();
}
