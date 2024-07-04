var Offline = {
  init: function () {
    if ("serviceWorker" in navigator) {
      window.addEventListener("load", function () {
        navigator.serviceWorker.register("/service-worker.js");
      });
    }
  },
};

export default Offline;
