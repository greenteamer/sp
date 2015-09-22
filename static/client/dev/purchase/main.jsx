var React = require('react');
var injectTapEventPlugin = require("react-tap-event-plugin");

var PurchaseDetail = require('../views/purchase/PurchaseDetail.jsx');
var PurchaseFilter = require('../views/filters/PurchaseFilter.jsx');
var CartMenu = require('../views/cartmenu/CartMenu.jsx');
var Cart = require('../views/cartmenu/Cart.jsx');
var SearchForm = require('../views/search/SearchForm.jsx');
var SearchResult = require('../views/search/SearchResult.jsx');
var Breadcrumbs = require('../views/breadcrumbs/Breadcrumbs.jsx');


injectTapEventPlugin();


React.render(<PurchaseDetail />, document.getElementById('purchase'));
React.render(<Breadcrumbs />, document.getElementById('breadcrumbs'));
React.render(<PurchaseFilter />, document.getElementById('filters'));
React.render(<CartMenu />, document.getElementById('cartmenu'));
React.render(<SearchForm />, document.getElementById('react_search'));
React.render(<SearchResult />, document.getElementById('react_search_result'));
