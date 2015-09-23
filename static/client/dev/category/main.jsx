var React = require('react');
var injectTapEventPlugin = require("react-tap-event-plugin");

var Category = require('../views/category/Category.jsx');
var Filters = require('../views/filters/Filters.jsx');
var CartMenu = require('../views/cartmenu/CartMenu.jsx');
var Cart = require('../views/cartmenu/Cart.jsx');
var SearchForm = require('../views/search/SearchForm.jsx');
var SearchResult = require('../views/search/SearchResult.jsx');
var Breadcrumbs = require('../views/breadcrumbs/Breadcrumbs.jsx');


injectTapEventPlugin();


React.render(<Category />, document.getElementById('category'));
React.render(<Breadcrumbs />, document.getElementById('breadcrumbs'));
React.render(<Filters />, document.getElementById('filters'));
React.render(<CartMenu />, document.getElementById('cartmenu'));
React.render(<SearchForm />, document.getElementById('react_search'));
React.render(<SearchResult />, document.getElementById('react_search_result'));
