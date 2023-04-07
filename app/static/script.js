// BOOTSTRAP TOOLS ACTIVATION
const tooltipTriggerList = $('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(
  (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
);

const toastElList = $(".toast");
const toastList = [...toastElList].map(
  (toastEl) => new bootstrap.Toast(toastEl)
);

/** Moves results screen down if window too short, otherwise gets
 * set to window height (#first-screen height is 100vh) */
function repositionScreen2() {
  $("#second-screen").offset({ top: $("#first-screen").height() });
}
$(window).on("resize", repositionScreen2);
repositionScreen2();

/** Set num of decimals in relation to size of price except
 * if small price or numDecimals already selected (default 8)*/
function formatPrice(price, numDecimals = 8) {
  if (price >= 10 && numDecimals == 8) {
    // Count number of digits before decimal point
    const numDigits = Math.floor(Math.log10(price) + 1);
    numDecimals = numDigits < 8 ? 9 - numDigits : 2;
  }

  // Create number formatter.
  const formatter = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: numDecimals,
    maximumFractionDigits: numDecimals,
  });

  return formatter.format(price).slice(1);
}

const $fsymRadios = $("input[name=fsym-radio]");
const $tsymRadios = $("input[name=tsym-radio]");
const $form = $("form");

$fsymRadios.on("change", changeSelects.bind(null, "fsym-"));
$tsymRadios.on("change", changeSelects.bind(null, "tsym-"));
$form.on("submit", handleForm);

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
  for (button of $fsymRadios) if (button.checked) break;
  for (button of $tsymRadios) if (button.checked) break;
  // From those, get the corresponding select
  const fromSelect = $($(button).data("target-select"));
  const toSelect = $($(button).data("target-select"));

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

  // Add data to result section
  $("#to-sym").text(to_sym);
  $("#usd-result").text(formatPrice(btcEquiv * currentBtcPrice));
  $("#btc-result").text(formatPrice(btcEquiv));
  $("#btc-price").text(formatPrice(btcPrice, 2));

  // Show result section and scroll to it
  $("#second-screen").removeClass("d-none")[0].scrollIntoView();
}
