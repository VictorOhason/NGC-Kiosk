const searchPanel = document.querySelector(".checkin-page__search-panel");
const searchInput = searchPanel?.querySelector(".checkin-page__input");
const searchForm = searchPanel?.querySelector(".checkin-page__form");
const searchStatus = searchForm?.querySelector(".checkin-page__status");
const searchButton = searchForm?.querySelector(".checkin-page__search-button");

searchPanel?.addEventListener("click", (event) => {
  if (
    event.target instanceof Element &&
    event.target.closest("button, input, a, select, textarea")
  ) {
    return;
  }

  searchInput?.focus();
});

searchForm?.addEventListener("submit", () => {
  if (!searchStatus || !searchButton) {
    return;
  }

  searchStatus.textContent = "Searching for your booking…";
  searchStatus.hidden = false;
  searchStatus.classList.remove("checkin-page__status--error");
  searchForm.setAttribute("aria-busy", "true");
  searchButton.disabled = true;
  searchButton.setAttribute("aria-busy", "true");
});

searchForm?.addEventListener("reset", () => {
  searchForm.removeAttribute("aria-busy");
  searchButton?.removeAttribute("aria-busy");
  if (searchButton) {
    searchButton.disabled = false;
  }
  if (searchStatus) {
    searchStatus.textContent = "";
    searchStatus.hidden = true;
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape" || !searchForm || !searchInput) {
    return;
  }

  event.preventDefault();
  searchForm.reset();
  searchInput.focus();
});

window.addEventListener("pageshow", (event) => {
  if (event.persisted && searchForm) {
    searchForm.reset();
  }
});
