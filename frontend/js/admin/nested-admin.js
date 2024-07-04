var $ = window.django.jQuery;

var NestedAdmin = {
  init: function () {
    $(document).on("formset:added", NestedAdmin.onAddComponent);
  },

  // this event is triggered called when both the 'add new component' and
  // the 'add another xxxxx' links are clicked
  // we want to filter only clicks on xxxxx components.
  onAddComponent: function (event, $row, formsetName) {
    // if this is an exercise component, we need to init ckeditor
    if (
      formsetName.toLowerCase().indexOf("exercise") !== -1 ||
      formsetName.toLowerCase().indexOf("step") !== -1
    ) {
      NestedAdmin.initCKEditor();
    }
  },

  // editorial/table blocks added by the component admin need to be manually
  // initialised.
  //
  // taken from:
  // https://github.com/django-ckeditor/django-ckeditor/blob/master/ckeditor/static/ckeditor/ckeditor-init.js
  initCKEditor: function () {
    var textareas = Array.prototype.slice.call(
      document.querySelectorAll("textarea[data-type=ckeditortype]"),
    );
    for (var i = 0; i < textareas.length; ++i) {
      var t = textareas[i];
      if (
        t.getAttribute("data-processed") == "0" &&
        t.id.indexOf("__prefix__") == -1
      ) {
        t.setAttribute("data-processed", "1");
        var ext = JSON.parse(t.getAttribute("data-external-plugin-resources"));
        for (var j = 0; j < ext.length; ++j) {
          window.CKEDITOR.plugins.addExternal(ext[j][0], ext[j][1], ext[j][2]);
        }
        window.CKEDITOR.replace(
          t.id,
          JSON.parse(t.getAttribute("data-config")),
        );
      }
    }
  },
};

export default NestedAdmin;
