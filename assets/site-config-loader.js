(function () {
  const cfg = window.MAKERSOLVE_CONFIG || {};

  function setText(selector, value) {
    if (!value) return;
    document.querySelectorAll(selector).forEach((el) => {
      el.textContent = value;
    });
  }

  function setHref(selector, value) {
    if (!value) return;
    document.querySelectorAll(selector).forEach((el) => {
      el.setAttribute("href", value);
    });
  }

  function removeIfEmpty(selector, value) {
    if (value) return;
    document.querySelectorAll(selector).forEach((el) => {
      el.remove();
    });
  }

  setText("[data-site-email]", cfg.email);
  setHref("[data-site-email-link]", cfg.email ? `mailto:${cfg.email}` : "");

  setText("[data-site-phone]", cfg.phoneDisplay);
  setHref("[data-site-phone-link]", cfg.phoneHref ? `tel:${cfg.phoneHref}` : "");
  removeIfEmpty("[data-phone-optional]", cfg.phoneDisplay);

  setText("[data-site-area]", cfg.serviceArea);
  setText("[data-site-city]", cfg.city);
  setText("[data-site-region]", cfg.region);
  setText("[data-site-vat]", cfg.vatNumber);
  removeIfEmpty("[data-vat-optional]", cfg.vatNumber);

  setHref("[data-site-linkedin-link]", cfg.linkedin);
})();
