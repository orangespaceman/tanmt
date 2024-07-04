var Header = {
  selectors: {
    root: ".js-Header",
    toggle: ".js-Header-toggle",
    nav: ".js-Header-nav",
  },
  els: {},

  init: function () {
    this.gatherEls();
    if (!this.els.toggle) return;
    this.els.toggle.addEventListener("click", this.toggleMenu.bind(this));
  },

  gatherEls: function () {
    Object.keys(this.selectors).forEach(this.gatherEl.bind(this));
  },

  gatherEl: function (selector) {
    var el = document.querySelector(this.selectors[selector]);
    if (el) {
      this.els[selector] = el;
    }
  },

  toggleMenu: function (e) {
    e.preventDefault();
    this.els.toggle.classList.toggle("is-active");
    this.els.nav.classList.toggle("is-active");
  },
};

export default Header;
