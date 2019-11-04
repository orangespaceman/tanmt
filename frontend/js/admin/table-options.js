var TableOptions = {
  init: function() {
    if (window.CKEDITOR) {
      window.CKEDITOR.on("dialogDefinition", function(ev) {
        var dialogName = ev.data.name;
        var dialogDefinition = ev.data.definition;

        if (dialogName === "table") {
          var infoTab = dialogDefinition.getContents("info");

          // hide most table fields
          infoTab.remove("cmbAlign");
          infoTab.remove("selHeaders");
          infoTab.remove("txtHeight");
          infoTab.remove("txtCellSpace");
          infoTab.remove("txtCellPad");
          infoTab.remove("txtCaption");
          infoTab.remove("txtSummary");

          // instead of hiding width field, default it to full editor width
          var widthField = infoTab.get("txtWidth");
          widthField["default"] = "100%";

          // these fields are useful for the edit view,
          // their styles are overridden on the side itself
          dialogDefinition.onShow = function() {
            this.getContentElement("info", "txtBorder").disable();
            this.getContentElement("info", "txtWidth").disable();
          };
        }
      });
    }
  }
};

module.exports = TableOptions;
