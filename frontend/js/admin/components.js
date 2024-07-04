var $ = window.django.jQuery;

var Components = {
  init: function () {
    Components.showInitialComponents();
    $(document).on("formset:added", Components.onAddComponent);
  },

  // when the page loads, if there are existing components,
  // hide their empty options (show only the prefilled form)
  showInitialComponents: function () {
    var $rows = $(
      ".djn-group-root > .djn-fieldset > .djn-items > .djn-inline-form",
    );
    $rows.each(function (counter, row) {
      var $row = $(row);

      // if all component types are empty, don't hide any options
      if ($row.find(".djn-inline-form:not(.djn-empty-form)").length < 1) return;

      // at least one component has been filled
      // it may already be saved (".has_original"),
      // or it may have form errors.
      // either way, display it and hide the rest
      var $emptyComponents = $row.find(".djn-inline-form.djn-empty-form");
      $emptyComponents.each(function (subCounter, emptyComponent) {
        var $emptyComponent = $(emptyComponent);
        var $fieldset = $emptyComponent.closest(".djn-group-nested");

        // ensure this only applies to component fieldsets
        if ($fieldset.attr("id").indexOf("components-") !== 0) {
          return;
        }

        if (
          $fieldset.find(
            ".djn-inline-form.has_original, .djn-inline-form:not(.djn-empty-form)",
          ).length < 1
        ) {
          $fieldset.hide();
        }
      });
    });
  },

  // this event is triggered called when both the 'add new component' and
  // the 'add another xxxxx' links are clicked
  // we want to filter only clicks on xxxxx components.
  //
  // when triggered, hide other component fieldsets - show only this one
  onAddComponent: function (event, $row, formsetName) {
    if (formsetName === "components") return;

    var $fieldset = $row.parent().closest(".djn-group-nested");
    var $childFieldsets = $fieldset.find(".djn-group-nested");
    var $form = $row.parent().closest(".djn-inline-form");
    $form.find(".djn-group-nested").not($fieldset).not($childFieldsets).hide();

    // if this is an editorial/table component, we also need to init ckeditor
    if (
      formsetName.toLowerCase().indexOf("editorial") !== -1 ||
      formsetName.toLowerCase().indexOf("image_with_text") !== -1 ||
      formsetName.toLowerCase().indexOf("table") !== -1
    ) {
      Components.initCKEditor();
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

export default Components;
