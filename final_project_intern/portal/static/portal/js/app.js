document.querySelectorAll(".toast").forEach(t => {
  setTimeout(() => t.classList.add("hide"), 3500);
});
document.querySelectorAll("input, textarea, select").forEach(el => {
  el.addEventListener("focus", () => el.parentElement?.classList.add("focused"));
  el.addEventListener("blur", () => el.parentElement?.classList.remove("focused"));
});
