var React = require('react');
//var Category = require('../views/PopularIndex.jsx');
var CartMenu = require('../views/cartmenu/CartMenu.jsx');
var SearchForm = require('../views/search/SearchForm.jsx');
var SearchResult = require('../views/search/SearchResult.jsx');
var Product = require('../views/product/Product.jsx');
var injectTapEventPlugin = require("react-tap-event-plugin");


injectTapEventPlugin();


React.render(
	React.createElement(Product, null),
	document.getElementById('product')
);


React.render(
	React.createElement(CartMenu, null),
	document.getElementById('cartmenu')
);


React.render(
	React.createElement(SearchForm, null),
	document.getElementById('react_search')
);


React.render(
	React.createElement(SearchResult, null),
	document.getElementById('react_search_result')
);


