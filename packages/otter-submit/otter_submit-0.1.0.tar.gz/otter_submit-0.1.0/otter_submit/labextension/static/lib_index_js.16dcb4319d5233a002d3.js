"use strict";
(self["webpackChunk_otter_submit_submit_button"] = self["webpackChunk_otter_submit_submit_button"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);

/**
 * The plugin registration information.
 */
const plugin = {
    id: '@otter-submit/submit-button:plugin',
    description: 'A JupyterLab extension used to submit notebooks for grading to otter-service.',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    activate: (app, notebookTracker) => {
        // Nothing is needed
        const { commands } = app;
        const command = 'otter-submit:submit';
        var nbpanel;
        notebookTracker.currentChanged.connect((tracker, panel) => {
            nbpanel = panel;
        });
        // Add a command
        commands.addCommand(command, {
            label: 'Submit for Grading',
            caption: 'Send your notebook to be graded',
            execute: (args) => {
                var nb = nbpanel === null || nbpanel === void 0 ? void 0 : nbpanel.context.model.toJSON();
                var payload = JSON.stringify({ 'nb': nb });
                var otherParam = {
                    headers: { "Content-Type": "application/json" },
                    body: payload,
                    method: "POST"
                };
                fetch('/services/gofer_nb/', otherParam)
                    // processes the response (in this case grabs text)
                    .then(response => { return response.text(); })
                    // processes the output of previous line (calling it data, then doing something with it)
                    .then(data => { console.log(data); alert(data); });
            }
        });
    }
};
/**
 * Export the plugin as default.
 */
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.16dcb4319d5233a002d3.js.map