document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    const escapeAction = document.querySelector("[data-kiosk-escape]");
    if (escapeAction) {
      event.preventDefault();
      escapeAction.click();
    }
    return;
  }

  if (event.key !== "Enter") {
    return;
  }

  const activeElement = document.activeElement;
  if (
    activeElement instanceof HTMLElement &&
    activeElement !== document.body &&
    activeElement !== document.documentElement
  ) {
    return;
  }

  const enterAction = document.querySelector("[data-kiosk-enter]");
  if (enterAction) {
    event.preventDefault();
    enterAction.click();
  }
});

window.addEventListener("pageshow", (event) => {
  if (
    event.persisted &&
    document.querySelector(".success-page__body, .error-page__body")
  ) {
    window.location.replace("/");
  }
});
