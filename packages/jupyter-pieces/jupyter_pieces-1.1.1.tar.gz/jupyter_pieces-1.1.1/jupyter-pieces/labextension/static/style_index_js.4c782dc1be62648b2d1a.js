"use strict";
(self["webpackChunkjupyter_pieces"] = self["webpackChunkjupyter_pieces"] || []).push([["style_index_js"],{

/***/ "./node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/sourceMaps.js */ "./node_modules/css-loader/dist/runtime/sourceMaps.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/getUrl.js */ "./node_modules/css-loader/dist/runtime/getUrl.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2__);
// Imports



var ___CSS_LOADER_URL_IMPORT_0___ = new URL(/* asset import */ __webpack_require__(/*! ./assets/expand_arrow.png */ "./style/assets/expand_arrow.png"), __webpack_require__.b);
var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_sourceMaps_js__WEBPACK_IMPORTED_MODULE_0___default()));
var ___CSS_LOADER_URL_REPLACEMENT_0___ = _node_modules_css_loader_dist_runtime_getUrl_js__WEBPACK_IMPORTED_MODULE_2___default()(___CSS_LOADER_URL_IMPORT_0___);
// Module
___CSS_LOADER_EXPORT___.push([module.id, `/*
    See the JupyterLab Developer Guide for useful CSS Patterns:

    https://jupyterlab.readthedocs.io/en/stable/developer/css.html
*/

* {
    box-sizing: border-box;
}

.jp-btn {
    cursor: pointer;
    -webkit-app-region: no-drag;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: var(--jp-inverse-layout-color3);
    font-size: 13px;
    border-radius: 5px;
    border: 0;
    padding: 4px 12px;
    height: 30px;
    width: fit-content;
    font-weight: 400;
    font-family: inherit;
    outline: none;
    user-select: none;
    white-space: nowrap;
    background-color: var(--jp-layout-color2);
    box-shadow: inset 0 0.5px 0.5px 0.5px rgba(255, 255, 255, 0.09),
        0 2px 4px 0 rgba(0, 0, 0, 0.15), 0 1px 1.5px 0 rgba(0, 0, 0, 0.1),
        0 1px 2px 0 rgba(0, 0, 0, 0.2), 0 0 0 0 transparent;
}

.delete-btn {
    background-color: var(--jp-layout-color1);
}

.jp-btn-transparent {
    -webkit-app-region: no-drag;
    display: inline-flex;
    align-items: center;
    background: none;
    border: none;
    color: var(--jp-inverse-layout-color3);
    cursor: pointer;
    padding: 0;
    user-select: none;
    position: sticky;
    width: fit-content;
    height: fit-content !important;
    left: 100%;
    top: 0%;
    z-index: 9998 !important;
}

.jp-dropdown-arrow {
    color: var(--jp-inverse-layout-color3);
    position: sticky;
    margin-top: 7px;
    margin-left: -18px;
    pointer-events: none;
}

.jp-dropdown {
    margin: 0px;
    cursor: pointer;
    width: fit-content;
    -webkit-app-region: no-drag;
    height: 30px;
    font-size: 13px;
    font-family: inherit;
    font-weight: 400;
    color: var(--jp-inverse-layout-color3);
    line-height: 1.3;
    padding: 0 1.9em 0 0.8em;
    max-width: 100%;
    box-sizing: border-box;
    border: 0;
    box-shadow: inset 0 0.5px 0.5px 0.5px rgba(255, 255, 255, 0.09),
        0 2px 4px 0 rgba(0, 0, 0, 0.15), 0 1px 1.5px 0 rgba(0, 0, 0, 0.1),
        0 1px 2px 0 rgba(0, 0, 0, 0.2), 0 0 0 0 transparent;
    border-radius: 5px;
    appearance: none;
    background-color: var(--jp-layout-color2);
    background-repeat: no-repeat, repeat;
    background-position: right 0.7em top 50%, 0 0;
    background-size: 0.65em auto, 100%;
}

.jp-dropdown:focus {
    border: none !important;
    box-shadow: none !important;
    background: var(--jp-layout-color3);
}

.jp-btn:hover,
.jp-dropdown:hover,
.hint-btn:hover {
    background-color: var(--jp-layout-color3);
}

.jp-textarea,
.jp-input[type='text'],
.jp-input[type='search'],
.jp-input[type='email'],
.jp-input[type='password'],
.jp-input[type='number'] {
    -webkit-app-region: no-drag;
    border: 1px solid #363636;
    color: inherit;
    font-family: inherit;
    padding: 4px 8px;
    font-size: 13px;
    border-radius: 5px;
    outline: none;
    height: 30px;
}

.body {
    font-family: Inter, monospace;
}

.break {
    flex-basis: 100%;
    height: 0;
}

.jp-gif {
    width: 80%;
    height: auto;
}

.jp-button {
    background-color: hsl(254, 80%, 68%);
    border: 1px solid #ccc;
    border-radius: 4px;
    color: #ccc;
    font-size: 13px;
    font-weight: 400;
    line-height: 1.42857;
    margin: 0;
    padding: 6px 12px;
    text-align: center;
    vertical-align: middle;
    white-space: nowrap;
    text-decoration: none;
    display: inline-block;
}

.jp-button:hover {
    background-color: hsl(254deg 77.48% 73.32%);
    color: #333;
}

.jp-pieces-onboarding {
    display: flex;
    background-color: #1e1e1e;
    height: 100%;
    width: 100%;
}

.jp-center {
    justify-content: center;
    align-items: center;
}

.jp-spacer {
    width: 50px !important;
}

.jp-space-between {
    justify-content: space-between;
}

.jp-col,
.jp-col-small {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.jp-row,
.jp-row-small,
.jp-row-short {
    display: flex;
    flex-direction: row;
    width: 100%;
}

.jp-row-small {
    width: 20%;
}

.jp-row-short {
    margin-bottom: -20px;
}

.jp-col-small {
    width: 20%;
}

.jp-right {
    justify-content: flex-end;
    margin-right: 12px;
}

.jp-left,
.jp-left-long {
    justify-content: flex-start;
    margin-left: 12px;
}

.jp-left-long {
    margin-left: 20px;
}

h1 {
    color: var(--jp-ui-font-color0);
    font-size: 2.5em;
    font-weight: bold;
}

h2 {
    color: var(--jp-ui-font-color1);
    font-size: 1.75em;
    font-weight: bold;
}

h3 {
    color: var(--jp-ui-font-color1);
    font-size: 1.5em;
    font-weight: bold;
}

h4 {
    color: var(--jp-ui-font-color1);
    font-size: 1.25em;
    font-weight: bold;
}

h5 {
    color: var(--jp-ui-font-color1);
    font-size: 1em;
    font-weight: bold;
}

h6 {
    color: var(--jp-ui-font-color2);
    font-size: 0.75em;
    font-weight: bold;
}

a {
    display: inline-block;
    border-radius: 4px;
}

iframe:focus {
    outline: none;
}

iframe[seamless] {
    display: block;
}

.search-box-div {
    position: absolute;
    background: var(--jp-layout-color1);
    z-index: 9999;
    width: 100%;
    margin-top: 27px;
}

.container-div {
    margin-top: 118px;
}

#piecesDiv {
    background-color: var(--jp-layout-color1);
    /* color: white; */
    height: 100%;
    overflow-y: scroll !important;
    overflow: hidden;
}

#piecesContainer {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: auto;
}

.parent-div-container {
    display: flex;
    height: 100%;
}

.background {
    position: absolute;
    background-color: var(--jp-layout-color1);
    height: 31px;
    width: -webkit-fill-available;
    z-index: 9999;
}

.ml-auto {
    margin-left: auto;
}

.mr-auto {
    margin-right: auto;
}

.piecesSnippet {
    border-bottom: solid var(--jp-border-width) var(--jp-border-color2);
    background: var(--jp-border-color3);
    padding-bottom: 1px;
    margin-bottom: -2px;
    cursor: pointer;
}

.piecesSnippet:last-child {
    border-bottom: none;
}

.piecesSnippet:hover {
    background-color: var(--jp-layout-color0);
}

.row {
    display: flex;
    flex-direction: row;
}

.col,
.col-sm,
.col-fit {
    display: flex;
    flex-direction: column;
    flex: 1;
}

.col-sm {
    flex: 0.125;
}

.col-sm-fixed {
    margin-left: 8px;
    align-items: flex-end !important;
    max-width: 20px;
}

.col-fit {
    max-width: fit-content;
}

.snippet-title {
    align-items: flex-start;
    margin-top: 2px;
    margin-bottom: 1px;
}

.snippet-title h4 {
    margin-left: 3px;
    margin-bottom: 1px;
    margin-top: 2px;
    padding-top: 3.5px;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    overflow: hidden;
    -webkit-line-clamp: 2;
    color: var(--jp-inverse-layour-color0);
}

.snippet-title p {
    display: flex;
    text-align: center;
    align-items: center;
    height: 100%;
}

.snippet-title-img {
    margin-left: 8px;
    background-size: 22px;
    min-width: 22px;
    min-height: 22px;
    margin-top: 4.5px;
}

.snippet-description {
    margin-top: 2px;
    margin-bottom: 4px;
    margin-left: 8px;
    color: var(--jp-inverse-border-color);
    margin-right: 8px;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 3;
    overflow: hidden;
    text-overflow: ellipsis;
    align-items: top;
}

.expand {
    appearance: none;
    -webkit-appearance: none;
    -moz-appearance: none;
    position: relative;
    outline: none;
    cursor: pointer;
    background-image: url(${___CSS_LOADER_URL_REPLACEMENT_0___});
    background-size: contain;
    width: 24px;
    height: 24px;
}

.expand:not(:checked) {
    transform: rotate(90deg);
}

.expand-top {
    display: flex;
}
.expand-top p {
    max-width: 80%;
}

.expand-label {
    margin-left: 8px;
    color: var(--jp-inverse-layout-color0);
}

.search-row {
    margin-top: 3px;
    margin-bottom: 10px;
    margin-left: 10px;
    margin-right: 10px;
}

.search-input {
    flex-grow: 1;
    margin-right: 8px;
    overflow-x: hidden;
    height: 46px;
    border-style: none;
    padding: 10px;
    font-size: 18px;
    margin-top: 10px;
    letter-spacing: 0px;
    outline: none;
    border-radius: 6px;
    transition: all 500ms cubic-bezier(0, 0.11, 0.35, 1.3);
    border-bottom: 1px solid rgba(255, 255, 255, 0.5);
    background-color: transparent;
    padding-right: 40px;
    color: var(--jp-inverse-layout-color0);
    font: caption !important;
}

.search-input::placeholder {
    color: var(--jp-layout-color4);
    font-size: 18px;
    letter-spacing: 0px;
    font-weight: 100;
    font-size: small;
}

.pieces-btn-search {
    margin-top: 10px;
    height: 30px;
    font-size: 13px;
    align-self: flex-end;
    pointer-events: painted;
}

.expand-hidden-wrapper {
    display: block;
}

.pieces-container {
    overflow: hidden;
    overflow-y: scroll;
    background-color: var(--jp-layout-color1);
}

.pieces-container::-webkit-scrollbar {
    display: none;
}

/* VIEWCODE BUTTON
SNIPPET
STYLES */

.jp-viewcode-container {
    align-items: center;
    margin-bottom: 0px;
    margin-top: -3px;
    display: flex;
}

.jp-viewcode-container span {
    color: var(--jp-inverse-layour-color0);
    font-size: small;
    z-index: 1;
    margin-left: -85px;
    cursor: pointer;
}

.jp-viewcode-input {
    display: block;
    z-index: -1 !important;
    height: 22px !important;
    width: 80px !important;
    margin-top: 3px !important;
    margin-left: 12px !important;
    opacity: 0;
    cursor: pointer !important;
}

/* CODE
SNIPPET
STYLES */

.snippet-parent::-webkit-scrollbar,
.snippet-raw::-webkit-scrollbar,
.snippet-raw-pre::-webkit-scrollbar,
.edit-snippet-raw-pre::-webkit-scrollbar {
    display: none;
}

.snippet {
    background-color: var(--jp-layout-color1);
    box-shadow: 0px 4px 8px 0px rgba(0, 0, 0, 0.8);
    border-radius: 5px;
    margin: 8px;
    overflow: hidden;
    max-width: 100%;
    padding: 10px;
}

.snippet-parent {
    border-radius: 5px;
    max-height: 190px;
    height: auto;
    overflow: hidden;
    overflow-y: scroll;
    white-space: nowrap;
    position: relative;
}

.snippet-line-div {
    width: fit-content;
    padding-left: 4px;
    padding-right: 4px;
    white-space: nowrap;
    top: 0;
    position: absolute;
    z-index: 1;
    text-align: right;
    border-right: var(--jp-toolbar-border-color) 1px dashed;
}

.snippet-line-nums {
    color: var(--jp-toolbar-border-color);
    font-family: Consolas, monospace;
    opacity: 0.9;
}

.snippet-raw {
    line-height: 1.33333333333335;
    overflow-x: scroll;
    margin-left: 12px;
    z-index: 0;
    margin-right: 1px;
    height: fit-content;
}

.snippet-raw-pre {
    font-family: Consolas, monospace;
    margin-top: 0px;
    overflow-x: scroll;
    display: inline-block;
    user-select: text;
    margin-left: 4px;
}

.snippet-btn-row {
    display: flex;
    justify-content: space-between;
    margin-top: 15.5px;
    width: 100%;
}

.snippet-btn-row-user {
    display: flex;
    flex-wrap: nowrap;
    justify-content: center;
}

.snippet-footer {
    display: flex;
}

.hori-break {
    height: 5px;
}

.vert-break {
    padding-left: 5px;
}

@keyframes bouncing-loader {
    to {
        opacity: 0.1;
        transform: translate3d(0, -4px, 0);
    }
}

.bouncing-loader,
.refresh-bouncing-loader,
.share-code-bouncing-loader {
    display: flex;
    justify-content: center;
    margin-top: -6px;
    height: 31px;
    width: 39px;
    margin-left: 2px;
}

.refresh-bouncing-loader {
    margin-top: 5px;
}

.bouncing-loader > div,
.refresh-bouncing-loader > div,
.share-code-bouncing-loader > div {
    margin-top: 18px !important;
    width: 8px;
    height: 8px;
    margin: 0rem 0.1rem;
    background: var(--jp-inverse-layout-color3);
    border-radius: 50%;
    animation: bouncing-loader 0.5s infinite alternate;
}

.bouncing-loader > div:nth-child(2),
.refresh-bouncing-loader > div:nth-child(2),
.share-code-bouncing-loader > div:nth-child(2) {
    animation-delay: 0.2s;
}

.bouncing-loader > div:nth-child(3),
.refresh-bouncing-loader > div:nth-child(3),
.share-code-bouncing-loader > div:nth-child(3) {
    animation-delay: 0.4s;
}

.snippet-expand-view {
    overflow: auto;
}

.snippet-expand-view > h2,
.snippet-expand-view > h5 {
    margin-left: 8px;
}

.snippet-expand-view > table > thead > tr > td {
    border: 1px solid var(--jp-inverse-layout-color3);
}

.snippet-expand-view > table {
    margin: 8px;
}

.snippet-expand-view > table > tbody > tr > td {
    border: 1px solid var(--jp-inverse-layout-color3);
}

.snippet-expand-view > pre {
    margin: 8px;
    padding: 10px;
    overflow: auto;
}

.snippet-expand-view > pre > code {
    text-shadow: none !important;
    font-family: var(--jp-code-font-family);
}

.code-element {
    text-shadow: none !important;
    font-family: var(--jp-code-font-family);
    overflow-x: auto !important;
    padding: 8px !important;
}

.code-element::-webkit-scrollbar {
    display: none;
}

.snippet-expand-pre-dark {
    background-color: var(--jp-layout-color1) !important;
}

.snippet-expand-pre-light {
    background-color: var(--jp-layout-color2) !important;
}

/* LANGUAGE
VIEW
STYLES */

.language-container {
    /* background-color: var(--background-modifier); */
    margin-top: 0px;
}

.language-view {
    border-bottom: solid var(--jp-border-width) var(--jp-border-color2);
    height: auto;
    z-index: -1;
    background: var(--jp-border-color3);
}

.language-title-div:hover {
    background-color: var(--jp-layout-color0);
}

.language-title-div {
    display: flex;
    vertical-align: middle;
    align-items: center;
    justify-content: left;
    height: 50px !important;
    margin-top: 0px !important;
    margin-bottom: 0px !important;
    position: relative;
}

.language-title-div h1 {
    font-size: 15px;
    position: absolute;
    top: 9px;
    left: 40px;
    height: 30px !important;
}

.language-title-div span {
    width: 30px;
    height: 30px !important;
    margin-top: 19px;
    margin-right: 0px;
    top: 0px;
    right: 0px;
    font-size: 12px;
}

.language-button-input {
    z-index: 999 !important;
    opacity: 0;
    cursor: pointer !important;
    top: 0;
    left: 0;
    order: -1;
    flex-grow: 1;
    height: 49px !important;
    margin: 0px 0px 0px 0px !important;
    width: 100% !important;
    position: absolute;
}
.language-title {
    align-items: center;
    margin-top: 9px;
    margin-bottom: 9px;
    min-width: 25px;
    min-height: 25px;
    background-size: 25px;
}

.language-title-img {
    margin-left: 0px;
    margin-right: 5px;
}

.logo-heading {
    background-size: contain;
    background-repeat: no-repeat;
    display: block;
    width: 200px;
    height: calc(200px * 0.202235); /*Adjust for the aspect ratio of the image*/
}

.illustration {
    background-size: contain;
    width: 228px;
    height: 228px;
}

/* SNIPPET VIEW STATES */

.load-error-state,
.loading-state,
.pieces-empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: left;
    padding: 10px;
    margin-top: 17vh;
    min-height: 100%;
    overflow: auto;
}

.pieces-empty-state p,
.load-error-state p,
.loading-state p {
    max-width: 200px;
    margin-top: 20px;
    margin-bottom: 20px;
}

.load-error-state button,
.loading-state button {
    width: 180px;
}

.pieces-empty-state p {
    margin-top: 15px;
    margin-bottom: 15px;
}

.load-error-state {
    display: flex;
    margin-top: 14vh;
    max-height: fit-content;
    min-height: 0;
}

.load-error-state-holder {
    max-width: 100%;
    min-width: 100%;
    overflow: hidden;
    overflow-y: scroll;
    margin-top: 75px;
    text-align: center;
}

.load-error-state::-webkit-scrollbar,
.load-error-state-holder::-webkit-scrollbar {
    display: none;
}

.load-error-content {
    margin-left: auto !important;
    margin-right: auto !important;
    text-align: left;
}

.pieces-empty-state {
    margin-top: 7vh;
}

.snippetConstraint {
    display: flex;
    max-width: 100%;
    margin: 30px;
    margin-top: 0px;
}

/* EDIT
MODAL
STYLES */

.edit-modal-container {
    -webkit-app-region: initial;
    display: flex;
    align-items: center;
    justify-content: center;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 50;
}

.edit-modal-background {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(10, 10, 10, 0.4);
    opacity: 0.85;
}

.edit-modal {
    --checkbox-size: 15px;
    background-color: var(--jp-layout-color1);
    border-radius: 10px;
    border: solid var(--jp-border-width) var(--jp-border-color2);
    padding: 16px;
    position: relative;
    min-height: 100px;
    width: 560px;
    max-width: 80vw;
    max-height: 85vh;
    display: flex;
    flex-direction: column;
    overflow: auto;
    box-shadow: 0px 1.8px 7.3px rgba(0, 0, 0, 0.071),
        0px 6.3px 24.7px rgba(0, 0, 0, 0.112), 0px 30px 90px rgba(0, 0, 0, 0.2);
    -webkit-app-region: no-drag;
}

.edit-modal-close-button {
    cursor: pointer;
    position: absolute;
    top: 6px;
    right: 6px;
    font-size: 24px;
    line-height: 20px;
    height: 24px;
    width: 24px;
    padding: 0 4px;
    border-radius: 4px;
    color: #bababa;
}

.edit-modal-content {
    flex: 1 1 auto;
    font-size: 15px;
    display: block;
}

.edit-modal-header:empty {
    display: none;
}

.edit-modal-header {
    font-size: x-large;
    opacity: 0.9;
    margin-bottom: 0.75em;
    margin-top: 10px;
    margin-left: 8px;
    margin-right: 8px;
    letter-spacing: -0.015em;
    font-weight: 700;
    text-align: left;
    line-height: 1.3;
    margin-block-start: 0.33em;
    margin-block-end: 0.33em;
}

.edit-title-label-row {
    justify-content: left;
}

.edit-title-label {
    margin-top: 10px;
    margin-bottom: 10px;
    font-size: smaller;
    opacity: 0.8;
}

.edit-dropdown {
    text-align: left !important;
    cursor: pointer;
    max-height: 50px !important;
    overflow-y: scroll;
    background: transparent !important;
    margin-left: 10px;
    margin-right: 10px;
}

.edit-title-input {
    background: transparent !important;
    font-weight: 600 !important;
    height: 100%;
    width: 100%;
    margin-left: 10px;
    margin-right: 10px;
}

#edit-snippet-parent {
    max-height: 400px !important;
}

.edit-snippet-raw-pre {
    font-family: Consolas, monospace;
    margin-top: 0px;
    overflow-x: scroll;
    display: inline-block;
    user-select: text;
    margin-left: 23px;
    line-height: 1.4255555555;
}

.edit-title-label {
    margin-top: 5px;
    margin-bottom: 8px;
    margin-left: 10px;
}

.edit-desc-row {
    display: flex;
    width: 100%;
    flex-direction: row;
    justify-content: center;
    padding-left: 8px;
    padding-right: 8px;
    background-color: var(--jp-layout-color1);
}

.edit-desc-col {
    display: flex;
    flex-direction: column;
    min-width: 100%;
    width: 512px;
    height: 111px;
    margin: 8px;
    background: var(--jp-layout-color1);
}

/* ONBOARDING
STYLES */

/* ONBOARDING */

.pieces-onboarding {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    overflow-y: scroll;
    overflow-x: hidden;
}
.pieces-onboarding .main {
    width: 65%;
    max-width: 800px;
    height: auto;
    display: block;
    margin-top: 0; /* Reset the default margin */
    margin-bottom: auto; /* Push .main to the top */
}
.pieces-onboarding .main > * {
    opacity: 0; /* Initially hide the content */
    animation: fade-in 1s ease-in-out forwards; /* Apply the fade-in animation */
}

@keyframes fade-in {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

.pieces-onboarding img,
.pieces-onboarding .img {
    width: 100%;
    margin: 0px;
    margin-top: 10px;
    border-radius: 7px;
    transition: 1s;
    background-size: contain;
    display: block;
}
.pieces-onboarding img:hover,
.pieces-onboarding .img:hover {
    width: calc(100% + 10px);
    transition: 1s;
}
.pieces-onboarding .img {
    min-height: 375px;
}
.pieces-onboarding .img:hover {
    min-height: calc(375px + 10px);
}

.pieces-onboarding .nav {
    width: 100%;
    margin-bottom: 10px;
    margin-top: -10px;
    display: flex;
    align-items: center;
    justify-content: center;
}
.pieces-onboarding .nav a {
    margin: 10px;
}

.pieces-onboarding a {
    text-decoration: underline !important;
    margin: 0px;
    transition: 0.2s;
}
.pieces-onboarding a:hover {
    color: hsl(202, 62%, 34%);
    transition: 0.2s;
}

.pieces-onboarding .hero {
    width: 100%;
    margin: 0px;
    padding: 0px;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    position: relative;
    padding-bottom: 56.25%; /* 16:9 */
    height: 0;
}
.pieces-onboarding .hero iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}
.pieces-onboarding h1 {
    text-align: center;
}

/* DELETE
MODAL
STYLES */

.delete-modal-title {
    color: #f44336;
    opacity: 0.8;
    font-size: 2em;
}

.delete-modal-label {
    margin-top: 5px;
    margin-bottom: 8px;
    margin-left: 10px;
    letter-spacing: -0.015em;
    font-size: 1.37em;
    color: inherit;
    font-weight: 600;
}

.delete-desc-row {
    display: flex;
    width: 100%;
    flex-direction: row;
    justify-content: right;
    padding-left: 8px;
    padding-right: 8px;
    background-color: var(--jp-layout-color1);
}

.delete-del-btn {
    color: #ffffff;
    background-color: #f44336 !important;
    width: 80px;
    height: 40px;
    pointer-events: painted;
    font-size: medium;
}

.title-container-div {
    position: absolute;
}

.container {
    width: 250px;
    height: 40;
    box-shadow: 0px 2px 4px black;
    background: var(--background-secondary);
    overflow: hidden;
    z-index: 3;
    transition: all 1s;
    place-items: center;
    display: grid;
}

nav {
    position: absolute;
    top: 0%;
    left: 0;
    width: 100%;
    height: 40px;
    display: flex;
    justify-content: space-evenly;
    z-index: 99999999;
    background: transparent;
    color: rgb(150, 240, 177);
}
nav a {
    padding: 10px;
    text-decoration: none;
    color: gray;
    font-size: 1.4rem;
}

.content {
    display: flex;
    width: 750px;
    height: 100%;
}
.item {
    width: 250px;
    color: black;
    background: var(--background-secondary);
    display: flex;
    row-gap: 25px;
    justify-content: center;
    flex-direction: column;
    align-items: center;
}

.link {
    transition: all 0.3s;
}
.tabone {
    color: rgb(22, 22, 22);
    transform: scale(1.25);
}
.item {
    font-weight: bolder;
    font-size: 3rem;
    color: rgb(12, 12, 12);
}
.item1 {
    background-color: rgb(243, 118, 160);
}
.item2 {
    background-color: rgb(146, 146, 228);
}

.wrapper {
    position: absolute;
    z-index: 9999999;
    width: -webkit-fill-available;
    display: flex;
    justify-content: center;
    margin-top: 6px;
}

.wrapper-scroll-buffer {
    padding-right: 31px !important;
}

:root {
    --primary-color: #111;
    --secondary-color: #a8adb3;
}

.container {
    position: absolute;
    left: 0;
    top: 0;
    right: 0;
    bottom: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}

.tabs {
    display: flex;
    position: relative;
    background-color: var(--jp-layout-color2);
    border-radius: 6px;
    height: 28px;
    width: 100px;
    box-shadow: inset 0 0.5px 0.5px 0.5px rgba(255, 255, 255, 0.09),
        0 2px 4px 0 rgba(0, 0, 0, 0.15), 0 1px 1.5px 0 rgba(0, 0, 0, 0.1),
        0 1px 2px 0 rgba(0, 0, 0, 0.2), 0 0 0 0 transparent;
}

.tabs .aiSVG {
    margin-left: 8px;
}

.tabs * {
    z-index: 2;
}

input[type='radio'] {
    display: none;
}

.tab {
    display: flex;
    align-items: flex-end;
    justify-content: center;
    vertical-align: center;
    align-items: center;
    height: 100%;
    width: 100%;
    border-radius: 6px;
    cursor: pointer;
    transition: color 0.15s ease-in;
    letter-spacing: 0.01em;
}

input[type='radio']:checked + .tab {
    color: var(--primary-color);
}

input[type='radio']:checked + .tab svg {
    color: var(--primary-color);
}

input[id='radio-1']:checked ~ .glider {
    transform: translateX(0);
}

input[id='radio-2']:checked ~ .glider {
    transform: translateX(101%);
}

.glider {
    position: absolute;
    display: flex;
    height: 100%;
    background-color: var(--jp-inverse-layout-color3);
    border: 1px solid #363636;
    width: 50%;
    z-index: 1;
    border-radius: 6px;
    transition: 0.25s ease-out;
    top: 0px;
    left: 0px;
    box-shadow: inset 0 0.5px 0.5px 0.5px rgba(255, 255, 255, 0.09),
        0 2px 4px 0 rgba(0, 0, 0, 0.15), 0 1px 1.5px 0 rgba(0, 0, 0, 0.1),
        0 1px 2px 0 rgba(0, 0, 0, 0.2), 0 0 0 0 transparent;
}

.tabs svg {
    color: var(--text-normal);
    pointer-events: none;
}

#tab-1 svg,
#tab-2 svg {
    height: 18px;
    width: 18px;
    stroke-width: 1.75px;
    pointer-events: none;
}

#tab-2 svg {
    height: 21px;
    width: 21px;
}

.sliderDiv {
    display: flex;
    position: absolute;
    width: 100%;
    padding-right: 30px;
    margin-top: -3px;
}

/* Pieces
GPT
Styles */

.gpt-row,
.gpt-row-full,
.gpt-row-small,
.gpt-row-response {
    display: flex;
    flex-direction: row;
    max-width: 100%;
}

.gpt-row-response {
    height: fit-content;
}

.gpt-col,
.gpt-col-reverse,
.gpt-col-small {
    display: flex;
    flex-direction: column;
    max-width: 100%;
    min-width: 100%;
}

.gpt-col-small {
    min-width: 0;
}

.gpt-col-fill {
    flex: 1 !important;
}

.gpt-col-reverse {
    flex-direction: column-reverse;
}

.gpt-container {
    height: 100%;
    margin: 0;
    display: flex;
    min-width: 100%;
}

.gpt-input {
    background-color: var(--background-secondary);
    height: fit-content;
    padding-top: 16px;
    padding-bottom: 16px;
    padding-left: 16px;
    border: 1px;
    justify-content: center;
    align-items: flex-start;
    border-radius: 10px;
    box-shadow: 0px 4px 8px 0px rgba(0, 0, 0, 0.8);
    margin-top: 16px;
    margin-bottom: 16px;
    margin-left: 8px;
    margin-right: 8px;
}
.gpt-input-textarea::-webkit-scrollbar {
    display: none;
}

.gpt-input-textarea:focus {
    outline: none;
    border: none;
}

.gpt-input-textarea {
    display: block;
    width: 100%;
    overflow: hidden;
    line-height: 20px;
    cursor: text;
    overflow-wrap: break-word;
    resize: none;
    max-height: 100px;
    overflow-y: scroll;
    font-family: inherit;
    font-size: inherit;
    padding-right: 48px;
    text-align: start;
}

.gpt-input-textarea[contenteditable]:empty::before {
    content: 'Paste some code or ask a technical question...';
    color: gray;
}

.gpt-text-content {
    flex: 1;
    padding: 26px;
    border-radius: 10px;
    word-wrap: break-word;
    overflow-y: scroll;
    padding-bottom: 0px;
    min-height: 50%;
    margin-top: -18px;
}

.gpt-text-area {
    max-height: initial;
    height: 100%;
    overflow-y: scroll;
}

.gpt-text-div {
    display: flex;
    flex-direction: column;
    flex-basis: 100%;
    overflow-y: scroll;
    background-color: var(--background-secondary);
    border-radius: 10px;
    box-shadow: 0px 4px 8px 0px rgba(0, 0, 0, 0.8);
    margin-top: 41px;
    margin-left: 8px;
    margin-right: 8px;
}

.gpt-text-div::-webkit-scrollbar,
.gpt-text-content::-webkit-scrollbar,
.gpt-text-area::-webkit-scrollbar {
    display: none;
}

.gpt-text-response {
    padding: 12px;
    border-radius: 10px;
    text-align: left;
    margin-top: 0px;
    width: fit-content;
    word-break: break-word;
    margin-bottom: 10px;
    font-size: 14px;
    user-select: text;
}

.gpt-right-align {
    justify-content: flex-end;
}

.gpt-left-align {
    justify-content: flex-start;
}

.gpt-query {
    margin-right: 8px;
    background-color: var(--md-blue-400);
}

.gpt-response {
    margin-left: 8px;
    background-color: var(--jp-layout-color2);
    min-width: 0;
}

.gpt-img,
.gpt-img-small {
    width: 30px !important;
    height: 30px !important;
    justify-content: center;
    display: flex;
    min-width: 0;
}

.gpt-img-small {
    width: 0 !important;
    height: 0 !important;
}

#user-img svg,
#ai-img svg {
    width: 30px !important;
    height: 30px !important;
    color: var(--text-muted);
    margin-top: 6px;
}

.gpt-img-small svg {
    width: 25px !important;
    height: 25px !important;
    color: gray;
    position: absolute;
    right: 17px;
    bottom: 30px;
    cursor: pointer;
}

.gpt-btn-icon {
    align-items: center;
    display: flex;
    width: 21px;
    height: 21px;
}

.gpt-icon svg {
    width: 25px !important;
    height: 25px !important;
    color: gray;
    position: absolute;
    right: 23px;
    bottom: 54px;
}

.gpt-icon-file {
    width: 14px;
    height: 14px;
}

.gpt-icon-drift {
    margin-right: -12px;
}

.gpt-cancel {
    width: fit-content;
    color: gray;
    font-size: smaller;
    cursor: pointer;
    align-self: self-end;
    margin-right: 10px;
    margin-bottom: 7px;
    margin-top: 5px;
    position: sticky;
    bottom: 0;
    right: 0;
}

.gpt-text-intro {
    width: 100%;
    height: 100%;
    justify-content: center;
    display: flex;
    align-items: center;
    padding-left: 6px;
    padding-right: 6px;
}

.gpt-text-intro-content {
    text-align: center;
    padding: 5px;
    user-select: none;
}

.gpt-text-intro-title {
    font-size: 32px;
    font-weight: 600;
    margin-bottom: 5px;
}

.gpt-text-intro-title-div {
    padding-left: 10%;
    padding-right: 10%;
    margin-top: -40px;
    margin-bottom: -20px;
}

.gpt-parent {
    height: 100%;
}

.hint-btn,
.hint-btn-file {
    border: none;
    background-color: var(--jp-layout-color2);
    color: var(--text-normal);
    padding: 16px 30px;
    text-align: center;
    text-decoration: none;
    display: inline-flex;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 16px;
    align-items: center;
    font-size: 12px;
    white-space: normal;
    overflow: hidden;
    word-break: break-word;
    box-shadow: none !important;
    height: 30px;
}

.hint-btn-file {
    padding: 15px 25px;
    padding-left: 16px;
    background-color: var(--jp-layout-color3);
}

.hint-btn-file:hover {
    background-color: var(--jp-layout-color4);
}

#gpt-hints-container {
    justify-content: center;
    padding-left: 20px;
    padding-right: 20px;
}

.hint-title {
    color: var(--jp-content-font-color2);
    align-self: flex-start;
    font-size: 12px;
    margin: 2px;
    margin-left: 10px;
    justify-content: center;
}

.hint-title-file {
    font-weight: 400;
    font-size: 12px;
    color: var(--jp-content-font-color2);
}

.hint-list {
    max-height: 77px;
    overflow: hidden;
    overflow-y: scroll;
    border-radius: 5px;
    margin-left: 8px;
    margin-right: 8px;
    min-height: 20%;
}

.hint-list-file {
    max-height: 82px;
    overflow: hidden;
    overflow-y: scroll;
    border-color: var(--background-modifier-border);
    border-radius: 5px;
    margin-top: -12px;
    margin-bottom: -8px;
}

.hint-list::-webkit-scrollbar,
.hint-list-file::-webkit-scrollbar {
    display: none;
}

.hint-btn-text {
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2; /* Number of lines to show */
    -webkit-box-orient: vertical;
    margin-right: 6px;
    margin-left: -4px;
}

.gpt-response pre code {
    user-select: text;
    background-color: var(--jp-cell-editor-background);
    border-radius: 5px;
    box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.8);
    margin-top: 8px;
    margin-bottom: 12px;
    width: 100%;
    overflow: hidden;
    font-family: var(--jp-code-font-family);
    word-break: break-word;
    white-space: pre-line;
}

.gpt-response code {
    display: inline;
    white-space: pre-line;
    background-color: var(--jp-border-color0);
    padding-left: 4px;
    border-radius: 5px;
    padding-right: 4px;
}

.gpt-response-margin-delete {
    margin: 0px;
}

.gpt-response-button-div {
    margin-top: 14px;
    margin-bottom: 7px;
}

.icon-div {
    height: 20px;
    width: 20px;
}

.gpt-img-logo svg {
    background-size: contain;
    width: 152.5px;
    height: 63px;
    opacity: 0.9;
}

.save-to-pieces-holder {
    display: flex;
    flex-wrap: wrap-reverse;
    justify-content: flex-end;
    margin-top: -12px;
    margin-bottom: -11px;
}

.collapsed-pieces-holder {
    display: flex;
    margin-top: 0px;
    margin-right: 0px;
    overflow: hidden;
    overflow-y: visible;
    transform: rotate(0deg);
    transition: all 0.5s;
}

.collapsed-pieces-holder.collapsed {
    flex-wrap: nowrap;
    width: 0;
    transition: all 0.5s;
}

.collapsed-pieces-holder.expanded {
    flex-wrap: wrap;
}

.collapsed-pieces-holder + button svg {
    transform: rotate(0deg);
    transition: all 0.5s;
}

.collapsed-pieces-holder.collapsed + button svg {
    transform: rotate(360deg);
    transition: all 0.5s;
}

.gpt-button-div {
    margin-right: 4px;
}

.gpt-button-div svg {
    width: 17px;
    height: 17px;
}

.gpt-user-image {
    border-radius: 50%;
    width: 24px;
    height: 24px;
    margin-top: 5px;
}

.gpt-rel-wrap {
    flex-wrap: wrap;
}

.gpt-hint-col {
    border-radius: 5px;
}

.gpt-hint-row {
    padding-top: 7px;
}

.gpt-send-active {
    color: var(--md-blue-400) !important;
}

.gpt-send-unactive {
    color: gray;
}
`, "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"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","sourcesContent":["/*\n    See the JupyterLab Developer Guide for useful CSS Patterns:\n\n    https://jupyterlab.readthedocs.io/en/stable/developer/css.html\n*/\n\n* {\n    box-sizing: border-box;\n}\n\n.jp-btn {\n    cursor: pointer;\n    -webkit-app-region: no-drag;\n    display: inline-flex;\n    align-items: center;\n    justify-content: center;\n    color: var(--jp-inverse-layout-color3);\n    font-size: 13px;\n    border-radius: 5px;\n    border: 0;\n    padding: 4px 12px;\n    height: 30px;\n    width: fit-content;\n    font-weight: 400;\n    font-family: inherit;\n    outline: none;\n    user-select: none;\n    white-space: nowrap;\n    background-color: var(--jp-layout-color2);\n    box-shadow: inset 0 0.5px 0.5px 0.5px rgba(255, 255, 255, 0.09),\n        0 2px 4px 0 rgba(0, 0, 0, 0.15), 0 1px 1.5px 0 rgba(0, 0, 0, 0.1),\n        0 1px 2px 0 rgba(0, 0, 0, 0.2), 0 0 0 0 transparent;\n}\n\n.delete-btn {\n    background-color: var(--jp-layout-color1);\n}\n\n.jp-btn-transparent {\n    -webkit-app-region: no-drag;\n    display: inline-flex;\n    align-items: center;\n    background: none;\n    border: none;\n    color: var(--jp-inverse-layout-color3);\n    cursor: pointer;\n    padding: 0;\n    user-select: none;\n    position: sticky;\n    width: fit-content;\n    height: fit-content !important;\n    left: 100%;\n    top: 0%;\n    z-index: 9998 !important;\n}\n\n.jp-dropdown-arrow {\n    color: var(--jp-inverse-layout-color3);\n    position: sticky;\n    margin-top: 7px;\n    margin-left: -18px;\n    pointer-events: none;\n}\n\n.jp-dropdown {\n    margin: 0px;\n    cursor: pointer;\n    width: fit-content;\n    -webkit-app-region: no-drag;\n    height: 30px;\n    font-size: 13px;\n    font-family: inherit;\n    font-weight: 400;\n    color: var(--jp-inverse-layout-color3);\n    line-height: 1.3;\n    padding: 0 1.9em 0 0.8em;\n    max-width: 100%;\n    box-sizing: border-box;\n    border: 0;\n    box-shadow: inset 0 0.5px 0.5px 0.5px rgba(255, 255, 255, 0.09),\n        0 2px 4px 0 rgba(0, 0, 0, 0.15), 0 1px 1.5px 0 rgba(0, 0, 0, 0.1),\n        0 1px 2px 0 rgba(0, 0, 0, 0.2), 0 0 0 0 transparent;\n    border-radius: 5px;\n    appearance: none;\n    background-color: var(--jp-layout-color2);\n    background-repeat: no-repeat, repeat;\n    background-position: right 0.7em top 50%, 0 0;\n    background-size: 0.65em auto, 100%;\n}\n\n.jp-dropdown:focus {\n    border: none !important;\n    box-shadow: none !important;\n    background: var(--jp-layout-color3);\n}\n\n.jp-btn:hover,\n.jp-dropdown:hover,\n.hint-btn:hover {\n    background-color: var(--jp-layout-color3);\n}\n\n.jp-textarea,\n.jp-input[type='text'],\n.jp-input[type='search'],\n.jp-input[type='email'],\n.jp-input[type='password'],\n.jp-input[type='number'] {\n    -webkit-app-region: no-drag;\n    border: 1px solid #363636;\n    color: inherit;\n    font-family: inherit;\n    padding: 4px 8px;\n    font-size: 13px;\n    border-radius: 5px;\n    outline: none;\n    height: 30px;\n}\n\n.body {\n    font-family: Inter, monospace;\n}\n\n.break {\n    flex-basis: 100%;\n    height: 0;\n}\n\n.jp-gif {\n    width: 80%;\n    height: auto;\n}\n\n.jp-button {\n    background-color: hsl(254, 80%, 68%);\n    border: 1px solid #ccc;\n    border-radius: 4px;\n    color: #ccc;\n    font-size: 13px;\n    font-weight: 400;\n    line-height: 1.42857;\n    margin: 0;\n    padding: 6px 12px;\n    text-align: center;\n    vertical-align: middle;\n    white-space: nowrap;\n    text-decoration: none;\n    display: inline-block;\n}\n\n.jp-button:hover {\n    background-color: hsl(254deg 77.48% 73.32%);\n    color: #333;\n}\n\n.jp-pieces-onboarding {\n    display: flex;\n    background-color: #1e1e1e;\n    height: 100%;\n    width: 100%;\n}\n\n.jp-center {\n    justify-content: center;\n    align-items: center;\n}\n\n.jp-spacer {\n    width: 50px !important;\n}\n\n.jp-space-between {\n    justify-content: space-between;\n}\n\n.jp-col,\n.jp-col-small {\n    display: flex;\n    flex-direction: column;\n    height: 100%;\n}\n\n.jp-row,\n.jp-row-small,\n.jp-row-short {\n    display: flex;\n    flex-direction: row;\n    width: 100%;\n}\n\n.jp-row-small {\n    width: 20%;\n}\n\n.jp-row-short {\n    margin-bottom: -20px;\n}\n\n.jp-col-small {\n    width: 20%;\n}\n\n.jp-right {\n    justify-content: flex-end;\n    margin-right: 12px;\n}\n\n.jp-left,\n.jp-left-long {\n    justify-content: flex-start;\n    margin-left: 12px;\n}\n\n.jp-left-long {\n    margin-left: 20px;\n}\n\nh1 {\n    color: var(--jp-ui-font-color0);\n    font-size: 2.5em;\n    font-weight: bold;\n}\n\nh2 {\n    color: var(--jp-ui-font-color1);\n    font-size: 1.75em;\n    font-weight: bold;\n}\n\nh3 {\n    color: var(--jp-ui-font-color1);\n    font-size: 1.5em;\n    font-weight: bold;\n}\n\nh4 {\n    color: var(--jp-ui-font-color1);\n    font-size: 1.25em;\n    font-weight: bold;\n}\n\nh5 {\n    color: var(--jp-ui-font-color1);\n    font-size: 1em;\n    font-weight: bold;\n}\n\nh6 {\n    color: var(--jp-ui-font-color2);\n    font-size: 0.75em;\n    font-weight: bold;\n}\n\na {\n    display: inline-block;\n    border-radius: 4px;\n}\n\niframe:focus {\n    outline: none;\n}\n\niframe[seamless] {\n    display: block;\n}\n\n.search-box-div {\n    position: absolute;\n    background: var(--jp-layout-color1);\n    z-index: 9999;\n    width: 100%;\n    margin-top: 27px;\n}\n\n.container-div {\n    margin-top: 118px;\n}\n\n#piecesDiv {\n    background-color: var(--jp-layout-color1);\n    /* color: white; */\n    height: 100%;\n    overflow-y: scroll !important;\n    overflow: hidden;\n}\n\n#piecesContainer {\n    display: flex;\n    flex-direction: column;\n    height: 100%;\n    width: 100%;\n    overflow: auto;\n}\n\n.parent-div-container {\n    display: flex;\n    height: 100%;\n}\n\n.background {\n    position: absolute;\n    background-color: var(--jp-layout-color1);\n    height: 31px;\n    width: -webkit-fill-available;\n    z-index: 9999;\n}\n\n.ml-auto {\n    margin-left: auto;\n}\n\n.mr-auto {\n    margin-right: auto;\n}\n\n.piecesSnippet {\n    border-bottom: solid var(--jp-border-width) var(--jp-border-color2);\n    background: var(--jp-border-color3);\n    padding-bottom: 1px;\n    margin-bottom: -2px;\n    cursor: pointer;\n}\n\n.piecesSnippet:last-child {\n    border-bottom: none;\n}\n\n.piecesSnippet:hover {\n    background-color: var(--jp-layout-color0);\n}\n\n.row {\n    display: flex;\n    flex-direction: row;\n}\n\n.col,\n.col-sm,\n.col-fit {\n    display: flex;\n    flex-direction: column;\n    flex: 1;\n}\n\n.col-sm {\n    flex: 0.125;\n}\n\n.col-sm-fixed {\n    margin-left: 8px;\n    align-items: flex-end !important;\n    max-width: 20px;\n}\n\n.col-fit {\n    max-width: fit-content;\n}\n\n.snippet-title {\n    align-items: flex-start;\n    margin-top: 2px;\n    margin-bottom: 1px;\n}\n\n.snippet-title h4 {\n    margin-left: 3px;\n    margin-bottom: 1px;\n    margin-top: 2px;\n    padding-top: 3.5px;\n    display: -webkit-box;\n    -webkit-box-orient: vertical;\n    overflow: hidden;\n    -webkit-line-clamp: 2;\n    color: var(--jp-inverse-layour-color0);\n}\n\n.snippet-title p {\n    display: flex;\n    text-align: center;\n    align-items: center;\n    height: 100%;\n}\n\n.snippet-title-img {\n    margin-left: 8px;\n    background-size: 22px;\n    min-width: 22px;\n    min-height: 22px;\n    margin-top: 4.5px;\n}\n\n.snippet-description {\n    margin-top: 2px;\n    margin-bottom: 4px;\n    margin-left: 8px;\n    color: var(--jp-inverse-border-color);\n    margin-right: 8px;\n    display: -webkit-box;\n    -webkit-box-orient: vertical;\n    -webkit-line-clamp: 3;\n    overflow: hidden;\n    text-overflow: ellipsis;\n    align-items: top;\n}\n\n.expand {\n    appearance: none;\n    -webkit-appearance: none;\n    -moz-appearance: none;\n    position: relative;\n    outline: none;\n    cursor: pointer;\n    background-image: url('./assets/expand_arrow.png');\n    background-size: contain;\n    width: 24px;\n    height: 24px;\n}\n\n.expand:not(:checked) {\n    transform: rotate(90deg);\n}\n\n.expand-top {\n    display: flex;\n}\n.expand-top p {\n    max-width: 80%;\n}\n\n.expand-label {\n    margin-left: 8px;\n    color: var(--jp-inverse-layout-color0);\n}\n\n.search-row {\n    margin-top: 3px;\n    margin-bottom: 10px;\n    margin-left: 10px;\n    margin-right: 10px;\n}\n\n.search-input {\n    flex-grow: 1;\n    margin-right: 8px;\n    overflow-x: hidden;\n    height: 46px;\n    border-style: none;\n    padding: 10px;\n    font-size: 18px;\n    margin-top: 10px;\n    letter-spacing: 0px;\n    outline: none;\n    border-radius: 6px;\n    transition: all 500ms cubic-bezier(0, 0.11, 0.35, 1.3);\n    border-bottom: 1px solid rgba(255, 255, 255, 0.5);\n    background-color: transparent;\n    padding-right: 40px;\n    color: var(--jp-inverse-layout-color0);\n    font: caption !important;\n}\n\n.search-input::placeholder {\n    color: var(--jp-layout-color4);\n    font-size: 18px;\n    letter-spacing: 0px;\n    font-weight: 100;\n    font-size: small;\n}\n\n.pieces-btn-search {\n    margin-top: 10px;\n    height: 30px;\n    font-size: 13px;\n    align-self: flex-end;\n    pointer-events: painted;\n}\n\n.expand-hidden-wrapper {\n    display: block;\n}\n\n.pieces-container {\n    overflow: hidden;\n    overflow-y: scroll;\n    background-color: var(--jp-layout-color1);\n}\n\n.pieces-container::-webkit-scrollbar {\n    display: none;\n}\n\n/* VIEWCODE BUTTON\nSNIPPET\nSTYLES */\n\n.jp-viewcode-container {\n    align-items: center;\n    margin-bottom: 0px;\n    margin-top: -3px;\n    display: flex;\n}\n\n.jp-viewcode-container span {\n    color: var(--jp-inverse-layour-color0);\n    font-size: small;\n    z-index: 1;\n    margin-left: -85px;\n    cursor: pointer;\n}\n\n.jp-viewcode-input {\n    display: block;\n    z-index: -1 !important;\n    height: 22px !important;\n    width: 80px !important;\n    margin-top: 3px !important;\n    margin-left: 12px !important;\n    opacity: 0;\n    cursor: pointer !important;\n}\n\n/* CODE\nSNIPPET\nSTYLES */\n\n.snippet-parent::-webkit-scrollbar,\n.snippet-raw::-webkit-scrollbar,\n.snippet-raw-pre::-webkit-scrollbar,\n.edit-snippet-raw-pre::-webkit-scrollbar {\n    display: none;\n}\n\n.snippet {\n    background-color: var(--jp-layout-color1);\n    box-shadow: 0px 4px 8px 0px rgba(0, 0, 0, 0.8);\n    border-radius: 5px;\n    margin: 8px;\n    overflow: hidden;\n    max-width: 100%;\n    padding: 10px;\n}\n\n.snippet-parent {\n    border-radius: 5px;\n    max-height: 190px;\n    height: auto;\n    overflow: hidden;\n    overflow-y: scroll;\n    white-space: nowrap;\n    position: relative;\n}\n\n.snippet-line-div {\n    width: fit-content;\n    padding-left: 4px;\n    padding-right: 4px;\n    white-space: nowrap;\n    top: 0;\n    position: absolute;\n    z-index: 1;\n    text-align: right;\n    border-right: var(--jp-toolbar-border-color) 1px dashed;\n}\n\n.snippet-line-nums {\n    color: var(--jp-toolbar-border-color);\n    font-family: Consolas, monospace;\n    opacity: 0.9;\n}\n\n.snippet-raw {\n    line-height: 1.33333333333335;\n    overflow-x: scroll;\n    margin-left: 12px;\n    z-index: 0;\n    margin-right: 1px;\n    height: fit-content;\n}\n\n.snippet-raw-pre {\n    font-family: Consolas, monospace;\n    margin-top: 0px;\n    overflow-x: scroll;\n    display: inline-block;\n    user-select: text;\n    margin-left: 4px;\n}\n\n.snippet-btn-row {\n    display: flex;\n    justify-content: space-between;\n    margin-top: 15.5px;\n    width: 100%;\n}\n\n.snippet-btn-row-user {\n    display: flex;\n    flex-wrap: nowrap;\n    justify-content: center;\n}\n\n.snippet-footer {\n    display: flex;\n}\n\n.hori-break {\n    height: 5px;\n}\n\n.vert-break {\n    padding-left: 5px;\n}\n\n@keyframes bouncing-loader {\n    to {\n        opacity: 0.1;\n        transform: translate3d(0, -4px, 0);\n    }\n}\n\n.bouncing-loader,\n.refresh-bouncing-loader,\n.share-code-bouncing-loader {\n    display: flex;\n    justify-content: center;\n    margin-top: -6px;\n    height: 31px;\n    width: 39px;\n    margin-left: 2px;\n}\n\n.refresh-bouncing-loader {\n    margin-top: 5px;\n}\n\n.bouncing-loader > div,\n.refresh-bouncing-loader > div,\n.share-code-bouncing-loader > div {\n    margin-top: 18px !important;\n    width: 8px;\n    height: 8px;\n    margin: 0rem 0.1rem;\n    background: var(--jp-inverse-layout-color3);\n    border-radius: 50%;\n    animation: bouncing-loader 0.5s infinite alternate;\n}\n\n.bouncing-loader > div:nth-child(2),\n.refresh-bouncing-loader > div:nth-child(2),\n.share-code-bouncing-loader > div:nth-child(2) {\n    animation-delay: 0.2s;\n}\n\n.bouncing-loader > div:nth-child(3),\n.refresh-bouncing-loader > div:nth-child(3),\n.share-code-bouncing-loader > div:nth-child(3) {\n    animation-delay: 0.4s;\n}\n\n.snippet-expand-view {\n    overflow: auto;\n}\n\n.snippet-expand-view > h2,\n.snippet-expand-view > h5 {\n    margin-left: 8px;\n}\n\n.snippet-expand-view > table > thead > tr > td {\n    border: 1px solid var(--jp-inverse-layout-color3);\n}\n\n.snippet-expand-view > table {\n    margin: 8px;\n}\n\n.snippet-expand-view > table > tbody > tr > td {\n    border: 1px solid var(--jp-inverse-layout-color3);\n}\n\n.snippet-expand-view > pre {\n    margin: 8px;\n    padding: 10px;\n    overflow: auto;\n}\n\n.snippet-expand-view > pre > code {\n    text-shadow: none !important;\n    font-family: var(--jp-code-font-family);\n}\n\n.code-element {\n    text-shadow: none !important;\n    font-family: var(--jp-code-font-family);\n    overflow-x: auto !important;\n    padding: 8px !important;\n}\n\n.code-element::-webkit-scrollbar {\n    display: none;\n}\n\n.snippet-expand-pre-dark {\n    background-color: var(--jp-layout-color1) !important;\n}\n\n.snippet-expand-pre-light {\n    background-color: var(--jp-layout-color2) !important;\n}\n\n/* LANGUAGE\nVIEW\nSTYLES */\n\n.language-container {\n    /* background-color: var(--background-modifier); */\n    margin-top: 0px;\n}\n\n.language-view {\n    border-bottom: solid var(--jp-border-width) var(--jp-border-color2);\n    height: auto;\n    z-index: -1;\n    background: var(--jp-border-color3);\n}\n\n.language-title-div:hover {\n    background-color: var(--jp-layout-color0);\n}\n\n.language-title-div {\n    display: flex;\n    vertical-align: middle;\n    align-items: center;\n    justify-content: left;\n    height: 50px !important;\n    margin-top: 0px !important;\n    margin-bottom: 0px !important;\n    position: relative;\n}\n\n.language-title-div h1 {\n    font-size: 15px;\n    position: absolute;\n    top: 9px;\n    left: 40px;\n    height: 30px !important;\n}\n\n.language-title-div span {\n    width: 30px;\n    height: 30px !important;\n    margin-top: 19px;\n    margin-right: 0px;\n    top: 0px;\n    right: 0px;\n    font-size: 12px;\n}\n\n.language-button-input {\n    z-index: 999 !important;\n    opacity: 0;\n    cursor: pointer !important;\n    top: 0;\n    left: 0;\n    order: -1;\n    flex-grow: 1;\n    height: 49px !important;\n    margin: 0px 0px 0px 0px !important;\n    width: 100% !important;\n    position: absolute;\n}\n.language-title {\n    align-items: center;\n    margin-top: 9px;\n    margin-bottom: 9px;\n    min-width: 25px;\n    min-height: 25px;\n    background-size: 25px;\n}\n\n.language-title-img {\n    margin-left: 0px;\n    margin-right: 5px;\n}\n\n.logo-heading {\n    background-size: contain;\n    background-repeat: no-repeat;\n    display: block;\n    width: 200px;\n    height: calc(200px * 0.202235); /*Adjust for the aspect ratio of the image*/\n}\n\n.illustration {\n    background-size: contain;\n    width: 228px;\n    height: 228px;\n}\n\n/* SNIPPET VIEW STATES */\n\n.load-error-state,\n.loading-state,\n.pieces-empty-state {\n    display: flex;\n    flex-direction: column;\n    align-items: center;\n    justify-content: center;\n    text-align: left;\n    padding: 10px;\n    margin-top: 17vh;\n    min-height: 100%;\n    overflow: auto;\n}\n\n.pieces-empty-state p,\n.load-error-state p,\n.loading-state p {\n    max-width: 200px;\n    margin-top: 20px;\n    margin-bottom: 20px;\n}\n\n.load-error-state button,\n.loading-state button {\n    width: 180px;\n}\n\n.pieces-empty-state p {\n    margin-top: 15px;\n    margin-bottom: 15px;\n}\n\n.load-error-state {\n    display: flex;\n    margin-top: 14vh;\n    max-height: fit-content;\n    min-height: 0;\n}\n\n.load-error-state-holder {\n    max-width: 100%;\n    min-width: 100%;\n    overflow: hidden;\n    overflow-y: scroll;\n    margin-top: 75px;\n    text-align: center;\n}\n\n.load-error-state::-webkit-scrollbar,\n.load-error-state-holder::-webkit-scrollbar {\n    display: none;\n}\n\n.load-error-content {\n    margin-left: auto !important;\n    margin-right: auto !important;\n    text-align: left;\n}\n\n.pieces-empty-state {\n    margin-top: 7vh;\n}\n\n.snippetConstraint {\n    display: flex;\n    max-width: 100%;\n    margin: 30px;\n    margin-top: 0px;\n}\n\n/* EDIT\nMODAL\nSTYLES */\n\n.edit-modal-container {\n    -webkit-app-region: initial;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    position: absolute;\n    top: 0;\n    left: 0;\n    width: 100%;\n    height: 100%;\n    z-index: 50;\n}\n\n.edit-modal-background {\n    position: absolute;\n    top: 0;\n    left: 0;\n    width: 100%;\n    height: 100%;\n    background-color: rgba(10, 10, 10, 0.4);\n    opacity: 0.85;\n}\n\n.edit-modal {\n    --checkbox-size: 15px;\n    background-color: var(--jp-layout-color1);\n    border-radius: 10px;\n    border: solid var(--jp-border-width) var(--jp-border-color2);\n    padding: 16px;\n    position: relative;\n    min-height: 100px;\n    width: 560px;\n    max-width: 80vw;\n    max-height: 85vh;\n    display: flex;\n    flex-direction: column;\n    overflow: auto;\n    box-shadow: 0px 1.8px 7.3px rgba(0, 0, 0, 0.071),\n        0px 6.3px 24.7px rgba(0, 0, 0, 0.112), 0px 30px 90px rgba(0, 0, 0, 0.2);\n    -webkit-app-region: no-drag;\n}\n\n.edit-modal-close-button {\n    cursor: pointer;\n    position: absolute;\n    top: 6px;\n    right: 6px;\n    font-size: 24px;\n    line-height: 20px;\n    height: 24px;\n    width: 24px;\n    padding: 0 4px;\n    border-radius: 4px;\n    color: #bababa;\n}\n\n.edit-modal-content {\n    flex: 1 1 auto;\n    font-size: 15px;\n    display: block;\n}\n\n.edit-modal-header:empty {\n    display: none;\n}\n\n.edit-modal-header {\n    font-size: x-large;\n    opacity: 0.9;\n    margin-bottom: 0.75em;\n    margin-top: 10px;\n    margin-left: 8px;\n    margin-right: 8px;\n    letter-spacing: -0.015em;\n    font-weight: 700;\n    text-align: left;\n    line-height: 1.3;\n    margin-block-start: 0.33em;\n    margin-block-end: 0.33em;\n}\n\n.edit-title-label-row {\n    justify-content: left;\n}\n\n.edit-title-label {\n    margin-top: 10px;\n    margin-bottom: 10px;\n    font-size: smaller;\n    opacity: 0.8;\n}\n\n.edit-dropdown {\n    text-align: left !important;\n    cursor: pointer;\n    max-height: 50px !important;\n    overflow-y: scroll;\n    background: transparent !important;\n    margin-left: 10px;\n    margin-right: 10px;\n}\n\n.edit-title-input {\n    background: transparent !important;\n    font-weight: 600 !important;\n    height: 100%;\n    width: 100%;\n    margin-left: 10px;\n    margin-right: 10px;\n}\n\n#edit-snippet-parent {\n    max-height: 400px !important;\n}\n\n.edit-snippet-raw-pre {\n    font-family: Consolas, monospace;\n    margin-top: 0px;\n    overflow-x: scroll;\n    display: inline-block;\n    user-select: text;\n    margin-left: 23px;\n    line-height: 1.4255555555;\n}\n\n.edit-title-label {\n    margin-top: 5px;\n    margin-bottom: 8px;\n    margin-left: 10px;\n}\n\n.edit-desc-row {\n    display: flex;\n    width: 100%;\n    flex-direction: row;\n    justify-content: center;\n    padding-left: 8px;\n    padding-right: 8px;\n    background-color: var(--jp-layout-color1);\n}\n\n.edit-desc-col {\n    display: flex;\n    flex-direction: column;\n    min-width: 100%;\n    width: 512px;\n    height: 111px;\n    margin: 8px;\n    background: var(--jp-layout-color1);\n}\n\n/* ONBOARDING\nSTYLES */\n\n/* ONBOARDING */\n\n.pieces-onboarding {\n    height: 100%;\n    width: 100%;\n    display: flex;\n    flex-direction: column;\n    align-items: center;\n    justify-content: flex-start;\n    overflow-y: scroll;\n    overflow-x: hidden;\n}\n.pieces-onboarding .main {\n    width: 65%;\n    max-width: 800px;\n    height: auto;\n    display: block;\n    margin-top: 0; /* Reset the default margin */\n    margin-bottom: auto; /* Push .main to the top */\n}\n.pieces-onboarding .main > * {\n    opacity: 0; /* Initially hide the content */\n    animation: fade-in 1s ease-in-out forwards; /* Apply the fade-in animation */\n}\n\n@keyframes fade-in {\n    from {\n        opacity: 0;\n    }\n    to {\n        opacity: 1;\n    }\n}\n\n.pieces-onboarding img,\n.pieces-onboarding .img {\n    width: 100%;\n    margin: 0px;\n    margin-top: 10px;\n    border-radius: 7px;\n    transition: 1s;\n    background-size: contain;\n    display: block;\n}\n.pieces-onboarding img:hover,\n.pieces-onboarding .img:hover {\n    width: calc(100% + 10px);\n    transition: 1s;\n}\n.pieces-onboarding .img {\n    min-height: 375px;\n}\n.pieces-onboarding .img:hover {\n    min-height: calc(375px + 10px);\n}\n\n.pieces-onboarding .nav {\n    width: 100%;\n    margin-bottom: 10px;\n    margin-top: -10px;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n}\n.pieces-onboarding .nav a {\n    margin: 10px;\n}\n\n.pieces-onboarding a {\n    text-decoration: underline !important;\n    margin: 0px;\n    transition: 0.2s;\n}\n.pieces-onboarding a:hover {\n    color: hsl(202, 62%, 34%);\n    transition: 0.2s;\n}\n\n.pieces-onboarding .hero {\n    width: 100%;\n    margin: 0px;\n    padding: 0px;\n\n    display: flex;\n    flex-direction: column;\n    align-items: center;\n    justify-content: center;\n\n    position: relative;\n    padding-bottom: 56.25%; /* 16:9 */\n    height: 0;\n}\n.pieces-onboarding .hero iframe {\n    position: absolute;\n    top: 0;\n    left: 0;\n    width: 100%;\n    height: 100%;\n}\n.pieces-onboarding h1 {\n    text-align: center;\n}\n\n/* DELETE\nMODAL\nSTYLES */\n\n.delete-modal-title {\n    color: #f44336;\n    opacity: 0.8;\n    font-size: 2em;\n}\n\n.delete-modal-label {\n    margin-top: 5px;\n    margin-bottom: 8px;\n    margin-left: 10px;\n    letter-spacing: -0.015em;\n    font-size: 1.37em;\n    color: inherit;\n    font-weight: 600;\n}\n\n.delete-desc-row {\n    display: flex;\n    width: 100%;\n    flex-direction: row;\n    justify-content: right;\n    padding-left: 8px;\n    padding-right: 8px;\n    background-color: var(--jp-layout-color1);\n}\n\n.delete-del-btn {\n    color: #ffffff;\n    background-color: #f44336 !important;\n    width: 80px;\n    height: 40px;\n    pointer-events: painted;\n    font-size: medium;\n}\n\n.title-container-div {\n    position: absolute;\n}\n\n.container {\n    width: 250px;\n    height: 40;\n    box-shadow: 0px 2px 4px black;\n    background: var(--background-secondary);\n    overflow: hidden;\n    z-index: 3;\n    transition: all 1s;\n    place-items: center;\n    display: grid;\n}\n\nnav {\n    position: absolute;\n    top: 0%;\n    left: 0;\n    width: 100%;\n    height: 40px;\n    display: flex;\n    justify-content: space-evenly;\n    z-index: 99999999;\n    background: transparent;\n    color: rgb(150, 240, 177);\n}\nnav a {\n    padding: 10px;\n    text-decoration: none;\n    color: gray;\n    font-size: 1.4rem;\n}\n\n.content {\n    display: flex;\n    width: 750px;\n    height: 100%;\n}\n.item {\n    width: 250px;\n    color: black;\n    background: var(--background-secondary);\n    display: flex;\n    row-gap: 25px;\n    justify-content: center;\n    flex-direction: column;\n    align-items: center;\n}\n\n.link {\n    transition: all 0.3s;\n}\n.tabone {\n    color: rgb(22, 22, 22);\n    transform: scale(1.25);\n}\n.item {\n    font-weight: bolder;\n    font-size: 3rem;\n    color: rgb(12, 12, 12);\n}\n.item1 {\n    background-color: rgb(243, 118, 160);\n}\n.item2 {\n    background-color: rgb(146, 146, 228);\n}\n\n.wrapper {\n    position: absolute;\n    z-index: 9999999;\n    width: -webkit-fill-available;\n    display: flex;\n    justify-content: center;\n    margin-top: 6px;\n}\n\n.wrapper-scroll-buffer {\n    padding-right: 31px !important;\n}\n\n:root {\n    --primary-color: #111;\n    --secondary-color: #a8adb3;\n}\n\n.container {\n    position: absolute;\n    left: 0;\n    top: 0;\n    right: 0;\n    bottom: 0;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n}\n\n.tabs {\n    display: flex;\n    position: relative;\n    background-color: var(--jp-layout-color2);\n    border-radius: 6px;\n    height: 28px;\n    width: 100px;\n    box-shadow: inset 0 0.5px 0.5px 0.5px rgba(255, 255, 255, 0.09),\n        0 2px 4px 0 rgba(0, 0, 0, 0.15), 0 1px 1.5px 0 rgba(0, 0, 0, 0.1),\n        0 1px 2px 0 rgba(0, 0, 0, 0.2), 0 0 0 0 transparent;\n}\n\n.tabs .aiSVG {\n    margin-left: 8px;\n}\n\n.tabs * {\n    z-index: 2;\n}\n\ninput[type='radio'] {\n    display: none;\n}\n\n.tab {\n    display: flex;\n    align-items: flex-end;\n    justify-content: center;\n    vertical-align: center;\n    align-items: center;\n    height: 100%;\n    width: 100%;\n    border-radius: 6px;\n    cursor: pointer;\n    transition: color 0.15s ease-in;\n    letter-spacing: 0.01em;\n}\n\ninput[type='radio']:checked + .tab {\n    color: var(--primary-color);\n}\n\ninput[type='radio']:checked + .tab svg {\n    color: var(--primary-color);\n}\n\ninput[id='radio-1']:checked ~ .glider {\n    transform: translateX(0);\n}\n\ninput[id='radio-2']:checked ~ .glider {\n    transform: translateX(101%);\n}\n\n.glider {\n    position: absolute;\n    display: flex;\n    height: 100%;\n    background-color: var(--jp-inverse-layout-color3);\n    border: 1px solid #363636;\n    width: 50%;\n    z-index: 1;\n    border-radius: 6px;\n    transition: 0.25s ease-out;\n    top: 0px;\n    left: 0px;\n    box-shadow: inset 0 0.5px 0.5px 0.5px rgba(255, 255, 255, 0.09),\n        0 2px 4px 0 rgba(0, 0, 0, 0.15), 0 1px 1.5px 0 rgba(0, 0, 0, 0.1),\n        0 1px 2px 0 rgba(0, 0, 0, 0.2), 0 0 0 0 transparent;\n}\n\n.tabs svg {\n    color: var(--text-normal);\n    pointer-events: none;\n}\n\n#tab-1 svg,\n#tab-2 svg {\n    height: 18px;\n    width: 18px;\n    stroke-width: 1.75px;\n    pointer-events: none;\n}\n\n#tab-2 svg {\n    height: 21px;\n    width: 21px;\n}\n\n.sliderDiv {\n    display: flex;\n    position: absolute;\n    width: 100%;\n    padding-right: 30px;\n    margin-top: -3px;\n}\n\n/* Pieces\nGPT\nStyles */\n\n.gpt-row,\n.gpt-row-full,\n.gpt-row-small,\n.gpt-row-response {\n    display: flex;\n    flex-direction: row;\n    max-width: 100%;\n}\n\n.gpt-row-response {\n    height: fit-content;\n}\n\n.gpt-col,\n.gpt-col-reverse,\n.gpt-col-small {\n    display: flex;\n    flex-direction: column;\n    max-width: 100%;\n    min-width: 100%;\n}\n\n.gpt-col-small {\n    min-width: 0;\n}\n\n.gpt-col-fill {\n    flex: 1 !important;\n}\n\n.gpt-col-reverse {\n    flex-direction: column-reverse;\n}\n\n.gpt-container {\n    height: 100%;\n    margin: 0;\n    display: flex;\n    min-width: 100%;\n}\n\n.gpt-input {\n    background-color: var(--background-secondary);\n    height: fit-content;\n    padding-top: 16px;\n    padding-bottom: 16px;\n    padding-left: 16px;\n    border: 1px;\n    justify-content: center;\n    align-items: flex-start;\n    border-radius: 10px;\n    box-shadow: 0px 4px 8px 0px rgba(0, 0, 0, 0.8);\n    margin-top: 16px;\n    margin-bottom: 16px;\n    margin-left: 8px;\n    margin-right: 8px;\n}\n.gpt-input-textarea::-webkit-scrollbar {\n    display: none;\n}\n\n.gpt-input-textarea:focus {\n    outline: none;\n    border: none;\n}\n\n.gpt-input-textarea {\n    display: block;\n    width: 100%;\n    overflow: hidden;\n    line-height: 20px;\n    cursor: text;\n    overflow-wrap: break-word;\n    resize: none;\n    max-height: 100px;\n    overflow-y: scroll;\n    font-family: inherit;\n    font-size: inherit;\n    padding-right: 48px;\n    text-align: start;\n}\n\n.gpt-input-textarea[contenteditable]:empty::before {\n    content: 'Paste some code or ask a technical question...';\n    color: gray;\n}\n\n.gpt-text-content {\n    flex: 1;\n    padding: 26px;\n    border-radius: 10px;\n    word-wrap: break-word;\n    overflow-y: scroll;\n    padding-bottom: 0px;\n    min-height: 50%;\n    margin-top: -18px;\n}\n\n.gpt-text-area {\n    max-height: initial;\n    height: 100%;\n    overflow-y: scroll;\n}\n\n.gpt-text-div {\n    display: flex;\n    flex-direction: column;\n    flex-basis: 100%;\n    overflow-y: scroll;\n    background-color: var(--background-secondary);\n    border-radius: 10px;\n    box-shadow: 0px 4px 8px 0px rgba(0, 0, 0, 0.8);\n    margin-top: 41px;\n    margin-left: 8px;\n    margin-right: 8px;\n}\n\n.gpt-text-div::-webkit-scrollbar,\n.gpt-text-content::-webkit-scrollbar,\n.gpt-text-area::-webkit-scrollbar {\n    display: none;\n}\n\n.gpt-text-response {\n    padding: 12px;\n    border-radius: 10px;\n    text-align: left;\n    margin-top: 0px;\n    width: fit-content;\n    word-break: break-word;\n    margin-bottom: 10px;\n    font-size: 14px;\n    user-select: text;\n}\n\n.gpt-right-align {\n    justify-content: flex-end;\n}\n\n.gpt-left-align {\n    justify-content: flex-start;\n}\n\n.gpt-query {\n    margin-right: 8px;\n    background-color: var(--md-blue-400);\n}\n\n.gpt-response {\n    margin-left: 8px;\n    background-color: var(--jp-layout-color2);\n    min-width: 0;\n}\n\n.gpt-img,\n.gpt-img-small {\n    width: 30px !important;\n    height: 30px !important;\n    justify-content: center;\n    display: flex;\n    min-width: 0;\n}\n\n.gpt-img-small {\n    width: 0 !important;\n    height: 0 !important;\n}\n\n#user-img svg,\n#ai-img svg {\n    width: 30px !important;\n    height: 30px !important;\n    color: var(--text-muted);\n    margin-top: 6px;\n}\n\n.gpt-img-small svg {\n    width: 25px !important;\n    height: 25px !important;\n    color: gray;\n    position: absolute;\n    right: 17px;\n    bottom: 30px;\n    cursor: pointer;\n}\n\n.gpt-btn-icon {\n    align-items: center;\n    display: flex;\n    width: 21px;\n    height: 21px;\n}\n\n.gpt-icon svg {\n    width: 25px !important;\n    height: 25px !important;\n    color: gray;\n    position: absolute;\n    right: 23px;\n    bottom: 54px;\n}\n\n.gpt-icon-file {\n    width: 14px;\n    height: 14px;\n}\n\n.gpt-icon-drift {\n    margin-right: -12px;\n}\n\n.gpt-cancel {\n    width: fit-content;\n    color: gray;\n    font-size: smaller;\n    cursor: pointer;\n    align-self: self-end;\n    margin-right: 10px;\n    margin-bottom: 7px;\n    margin-top: 5px;\n    position: sticky;\n    bottom: 0;\n    right: 0;\n}\n\n.gpt-text-intro {\n    width: 100%;\n    height: 100%;\n    justify-content: center;\n    display: flex;\n    align-items: center;\n    padding-left: 6px;\n    padding-right: 6px;\n}\n\n.gpt-text-intro-content {\n    text-align: center;\n    padding: 5px;\n    user-select: none;\n}\n\n.gpt-text-intro-title {\n    font-size: 32px;\n    font-weight: 600;\n    margin-bottom: 5px;\n}\n\n.gpt-text-intro-title-div {\n    padding-left: 10%;\n    padding-right: 10%;\n    margin-top: -40px;\n    margin-bottom: -20px;\n}\n\n.gpt-parent {\n    height: 100%;\n}\n\n.hint-btn,\n.hint-btn-file {\n    border: none;\n    background-color: var(--jp-layout-color2);\n    color: var(--text-normal);\n    padding: 16px 30px;\n    text-align: center;\n    text-decoration: none;\n    display: inline-flex;\n    margin: 4px 2px;\n    cursor: pointer;\n    border-radius: 16px;\n    align-items: center;\n    font-size: 12px;\n    white-space: normal;\n    overflow: hidden;\n    word-break: break-word;\n    box-shadow: none !important;\n    height: 30px;\n}\n\n.hint-btn-file {\n    padding: 15px 25px;\n    padding-left: 16px;\n    background-color: var(--jp-layout-color3);\n}\n\n.hint-btn-file:hover {\n    background-color: var(--jp-layout-color4);\n}\n\n#gpt-hints-container {\n    justify-content: center;\n    padding-left: 20px;\n    padding-right: 20px;\n}\n\n.hint-title {\n    color: var(--jp-content-font-color2);\n    align-self: flex-start;\n    font-size: 12px;\n    margin: 2px;\n    margin-left: 10px;\n    justify-content: center;\n}\n\n.hint-title-file {\n    font-weight: 400;\n    font-size: 12px;\n    color: var(--jp-content-font-color2);\n}\n\n.hint-list {\n    max-height: 77px;\n    overflow: hidden;\n    overflow-y: scroll;\n    border-radius: 5px;\n    margin-left: 8px;\n    margin-right: 8px;\n    min-height: 20%;\n}\n\n.hint-list-file {\n    max-height: 82px;\n    overflow: hidden;\n    overflow-y: scroll;\n    border-color: var(--background-modifier-border);\n    border-radius: 5px;\n    margin-top: -12px;\n    margin-bottom: -8px;\n}\n\n.hint-list::-webkit-scrollbar,\n.hint-list-file::-webkit-scrollbar {\n    display: none;\n}\n\n.hint-btn-text {\n    text-overflow: ellipsis;\n    display: -webkit-box;\n    -webkit-line-clamp: 2; /* Number of lines to show */\n    -webkit-box-orient: vertical;\n    margin-right: 6px;\n    margin-left: -4px;\n}\n\n.gpt-response pre code {\n    user-select: text;\n    background-color: var(--jp-cell-editor-background);\n    border-radius: 5px;\n    box-shadow: 0px 2px 4px 0px rgba(0, 0, 0, 0.8);\n    margin-top: 8px;\n    margin-bottom: 12px;\n    width: 100%;\n    overflow: hidden;\n    font-family: var(--jp-code-font-family);\n    word-break: break-word;\n    white-space: pre-line;\n}\n\n.gpt-response code {\n    display: inline;\n    white-space: pre-line;\n    background-color: var(--jp-border-color0);\n    padding-left: 4px;\n    border-radius: 5px;\n    padding-right: 4px;\n}\n\n.gpt-response-margin-delete {\n    margin: 0px;\n}\n\n.gpt-response-button-div {\n    margin-top: 14px;\n    margin-bottom: 7px;\n}\n\n.icon-div {\n    height: 20px;\n    width: 20px;\n}\n\n.gpt-img-logo svg {\n    background-size: contain;\n    width: 152.5px;\n    height: 63px;\n    opacity: 0.9;\n}\n\n.save-to-pieces-holder {\n    display: flex;\n    flex-wrap: wrap-reverse;\n    justify-content: flex-end;\n    margin-top: -12px;\n    margin-bottom: -11px;\n}\n\n.collapsed-pieces-holder {\n    display: flex;\n    margin-top: 0px;\n    margin-right: 0px;\n    overflow: hidden;\n    overflow-y: visible;\n    transform: rotate(0deg);\n    transition: all 0.5s;\n}\n\n.collapsed-pieces-holder.collapsed {\n    flex-wrap: nowrap;\n    width: 0;\n    transition: all 0.5s;\n}\n\n.collapsed-pieces-holder.expanded {\n    flex-wrap: wrap;\n}\n\n.collapsed-pieces-holder + button svg {\n    transform: rotate(0deg);\n    transition: all 0.5s;\n}\n\n.collapsed-pieces-holder.collapsed + button svg {\n    transform: rotate(360deg);\n    transition: all 0.5s;\n}\n\n.gpt-button-div {\n    margin-right: 4px;\n}\n\n.gpt-button-div svg {\n    width: 17px;\n    height: 17px;\n}\n\n.gpt-user-image {\n    border-radius: 50%;\n    width: 24px;\n    height: 24px;\n    margin-top: 5px;\n}\n\n.gpt-rel-wrap {\n    flex-wrap: wrap;\n}\n\n.gpt-hint-col {\n    border-radius: 5px;\n}\n\n.gpt-hint-row {\n    padding-top: 7px;\n}\n\n.gpt-send-active {\n    color: var(--md-blue-400) !important;\n}\n\n.gpt-send-unactive {\n    color: gray;\n}\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {



/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
module.exports = function (cssWithMappingToString) {
  var list = [];

  // return the list of modules as css string
  list.toString = function toString() {
    return this.map(function (item) {
      var content = "";
      var needLayer = typeof item[5] !== "undefined";
      if (item[4]) {
        content += "@supports (".concat(item[4], ") {");
      }
      if (item[2]) {
        content += "@media ".concat(item[2], " {");
      }
      if (needLayer) {
        content += "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {");
      }
      content += cssWithMappingToString(item);
      if (needLayer) {
        content += "}";
      }
      if (item[2]) {
        content += "}";
      }
      if (item[4]) {
        content += "}";
      }
      return content;
    }).join("");
  };

  // import a list of modules into the list
  list.i = function i(modules, media, dedupe, supports, layer) {
    if (typeof modules === "string") {
      modules = [[null, modules, undefined]];
    }
    var alreadyImportedModules = {};
    if (dedupe) {
      for (var k = 0; k < this.length; k++) {
        var id = this[k][0];
        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }
    for (var _k = 0; _k < modules.length; _k++) {
      var item = [].concat(modules[_k]);
      if (dedupe && alreadyImportedModules[item[0]]) {
        continue;
      }
      if (typeof layer !== "undefined") {
        if (typeof item[5] === "undefined") {
          item[5] = layer;
        } else {
          item[1] = "@layer".concat(item[5].length > 0 ? " ".concat(item[5]) : "", " {").concat(item[1], "}");
          item[5] = layer;
        }
      }
      if (media) {
        if (!item[2]) {
          item[2] = media;
        } else {
          item[1] = "@media ".concat(item[2], " {").concat(item[1], "}");
          item[2] = media;
        }
      }
      if (supports) {
        if (!item[4]) {
          item[4] = "".concat(supports);
        } else {
          item[1] = "@supports (".concat(item[4], ") {").concat(item[1], "}");
          item[4] = supports;
        }
      }
      list.push(item);
    }
  };
  return list;
};

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/getUrl.js":
/*!********************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/getUrl.js ***!
  \********************************************************/
/***/ ((module) => {



module.exports = function (url, options) {
  if (!options) {
    options = {};
  }
  if (!url) {
    return url;
  }
  url = String(url.__esModule ? url.default : url);

  // If url is already wrapped in quotes, remove them
  if (/^['"].*['"]$/.test(url)) {
    url = url.slice(1, -1);
  }
  if (options.hash) {
    url += options.hash;
  }

  // Should url be wrapped?
  // See https://drafts.csswg.org/css-values-3/#urls
  if (/["'() \t\n]|(%20)/.test(url) || options.needQuotes) {
    return "\"".concat(url.replace(/"/g, '\\"').replace(/\n/g, "\\n"), "\"");
  }
  return url;
};

/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/sourceMaps.js":
/*!************************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/sourceMaps.js ***!
  \************************************************************/
/***/ ((module) => {



module.exports = function (item) {
  var content = item[1];
  var cssMapping = item[3];
  if (!cssMapping) {
    return content;
  }
  if (typeof btoa === "function") {
    var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(cssMapping))));
    var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
    var sourceMapping = "/*# ".concat(data, " */");
    return [content].concat([sourceMapping]).join("\n");
  }
  return [content].join("\n");
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module) => {



var stylesInDOM = [];
function getIndexByIdentifier(identifier) {
  var result = -1;
  for (var i = 0; i < stylesInDOM.length; i++) {
    if (stylesInDOM[i].identifier === identifier) {
      result = i;
      break;
    }
  }
  return result;
}
function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];
  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var indexByIdentifier = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3],
      supports: item[4],
      layer: item[5]
    };
    if (indexByIdentifier !== -1) {
      stylesInDOM[indexByIdentifier].references++;
      stylesInDOM[indexByIdentifier].updater(obj);
    } else {
      var updater = addElementStyle(obj, options);
      options.byIndex = i;
      stylesInDOM.splice(i, 0, {
        identifier: identifier,
        updater: updater,
        references: 1
      });
    }
    identifiers.push(identifier);
  }
  return identifiers;
}
function addElementStyle(obj, options) {
  var api = options.domAPI(options);
  api.update(obj);
  var updater = function updater(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap && newObj.supports === obj.supports && newObj.layer === obj.layer) {
        return;
      }
      api.update(obj = newObj);
    } else {
      api.remove();
    }
  };
  return updater;
}
module.exports = function (list, options) {
  options = options || {};
  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];
    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDOM[index].references--;
    }
    var newLastIdentifiers = modulesToDom(newList, options);
    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];
      var _index = getIndexByIdentifier(_identifier);
      if (stylesInDOM[_index].references === 0) {
        stylesInDOM[_index].updater();
        stylesInDOM.splice(_index, 1);
      }
    }
    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertBySelector.js":
/*!********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertBySelector.js ***!
  \********************************************************************/
/***/ ((module) => {



var memo = {};

/* istanbul ignore next  */
function getTarget(target) {
  if (typeof memo[target] === "undefined") {
    var styleTarget = document.querySelector(target);

    // Special case to return head of iframe instead of iframe itself
    if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
      try {
        // This will throw an exception if access to iframe is blocked
        // due to cross-origin restrictions
        styleTarget = styleTarget.contentDocument.head;
      } catch (e) {
        // istanbul ignore next
        styleTarget = null;
      }
    }
    memo[target] = styleTarget;
  }
  return memo[target];
}

/* istanbul ignore next  */
function insertBySelector(insert, style) {
  var target = getTarget(insert);
  if (!target) {
    throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
  }
  target.appendChild(style);
}
module.exports = insertBySelector;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/insertStyleElement.js":
/*!**********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/insertStyleElement.js ***!
  \**********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function insertStyleElement(options) {
  var element = document.createElement("style");
  options.setAttributes(element, options.attributes);
  options.insert(element, options.options);
  return element;
}
module.exports = insertStyleElement;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js":
/*!**********************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js ***!
  \**********************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {



/* istanbul ignore next  */
function setAttributesWithoutAttributes(styleElement) {
  var nonce =  true ? __webpack_require__.nc : 0;
  if (nonce) {
    styleElement.setAttribute("nonce", nonce);
  }
}
module.exports = setAttributesWithoutAttributes;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleDomAPI.js":
/*!***************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleDomAPI.js ***!
  \***************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function apply(styleElement, options, obj) {
  var css = "";
  if (obj.supports) {
    css += "@supports (".concat(obj.supports, ") {");
  }
  if (obj.media) {
    css += "@media ".concat(obj.media, " {");
  }
  var needLayer = typeof obj.layer !== "undefined";
  if (needLayer) {
    css += "@layer".concat(obj.layer.length > 0 ? " ".concat(obj.layer) : "", " {");
  }
  css += obj.css;
  if (needLayer) {
    css += "}";
  }
  if (obj.media) {
    css += "}";
  }
  if (obj.supports) {
    css += "}";
  }
  var sourceMap = obj.sourceMap;
  if (sourceMap && typeof btoa !== "undefined") {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  }

  // For old IE
  /* istanbul ignore if  */
  options.styleTagTransform(css, styleElement, options.options);
}
function removeStyleElement(styleElement) {
  // istanbul ignore if
  if (styleElement.parentNode === null) {
    return false;
  }
  styleElement.parentNode.removeChild(styleElement);
}

/* istanbul ignore next  */
function domAPI(options) {
  if (typeof document === "undefined") {
    return {
      update: function update() {},
      remove: function remove() {}
    };
  }
  var styleElement = options.insertStyleElement(options);
  return {
    update: function update(obj) {
      apply(styleElement, options, obj);
    },
    remove: function remove() {
      removeStyleElement(styleElement);
    }
  };
}
module.exports = domAPI;

/***/ }),

/***/ "./node_modules/style-loader/dist/runtime/styleTagTransform.js":
/*!*********************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/styleTagTransform.js ***!
  \*********************************************************************/
/***/ ((module) => {



/* istanbul ignore next  */
function styleTagTransform(css, styleElement) {
  if (styleElement.styleSheet) {
    styleElement.styleSheet.cssText = css;
  } else {
    while (styleElement.firstChild) {
      styleElement.removeChild(styleElement.firstChild);
    }
    styleElement.appendChild(document.createTextNode(css));
  }
}
module.exports = styleTagTransform;

/***/ }),

/***/ "./style/index.js":
/*!************************!*\
  !*** ./style/index.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _base_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./base.css */ "./style/base.css");



/***/ }),

/***/ "./style/base.css":
/*!************************!*\
  !*** ./style/base.css ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleDomAPI.js */ "./node_modules/style-loader/dist/runtime/styleDomAPI.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertBySelector.js */ "./node_modules/style-loader/dist/runtime/insertBySelector.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js */ "./node_modules/style-loader/dist/runtime/setAttributesWithoutAttributes.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/insertStyleElement.js */ "./node_modules/style-loader/dist/runtime/insertStyleElement.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/styleTagTransform.js */ "./node_modules/style-loader/dist/runtime/styleTagTransform.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");

      
      
      
      
      
      
      
      
      

var options = {};

options.styleTagTransform = (_node_modules_style_loader_dist_runtime_styleTagTransform_js__WEBPACK_IMPORTED_MODULE_5___default());
options.setAttributes = (_node_modules_style_loader_dist_runtime_setAttributesWithoutAttributes_js__WEBPACK_IMPORTED_MODULE_3___default());

      options.insert = _node_modules_style_loader_dist_runtime_insertBySelector_js__WEBPACK_IMPORTED_MODULE_2___default().bind(null, "head");
    
options.domAPI = (_node_modules_style_loader_dist_runtime_styleDomAPI_js__WEBPACK_IMPORTED_MODULE_1___default());
options.insertStyleElement = (_node_modules_style_loader_dist_runtime_insertStyleElement_js__WEBPACK_IMPORTED_MODULE_4___default());

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"], options);




       /* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"] && _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals ? _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_6__["default"].locals : undefined);


/***/ }),

/***/ "./style/assets/expand_arrow.png":
/*!***************************************!*\
  !*** ./style/assets/expand_arrow.png ***!
  \***************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__.p + "b48800d872dd01c17bee.png";

/***/ })

}]);
//# sourceMappingURL=style_index_js.4c782dc1be62648b2d1a.js.map