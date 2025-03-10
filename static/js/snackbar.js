// Show snackbar method
let snackbarTimeoutId;
function showSnackbar(message, type = "error") {
  // Snackbar
  let snackbar = document.getElementById("snackbar")
  snackbar.className = "show"
  snackbar.innerHTML = message
  if (type === "error") {
    snackbar.style.backgroundColor = "#ff4444"
  } else if (type === "success") {
    snackbar.style.backgroundColor = "#3dbb56"
  }

  clearTimeout(snackbarTimeoutId);
  snackbarTimeoutId = setTimeout(function () {
    snackbar.className = snackbar.className.replace("show", "")
  }, 3000);
}