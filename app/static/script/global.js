// BOOTSTRAP TOOLS ACTIVATION
const tooltipTriggerList = $('[data-bs-toggle="tooltip"]');
const tooltipList = [...tooltipTriggerList].map(
  (tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl)
);

const toastElList = $(".toast");
const toastList = [...toastElList].map(
  (toastEl) => new bootstrap.Toast(toastEl)
);

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
