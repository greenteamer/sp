var React = require('react');
//var Category = require('../views/PopularIndex.jsx');
var CartMenu = require('../views/cartmenu/CartMenu.jsx');
var SearchForm = require('../views/search/SearchForm.jsx');
var SearchResult = require('../views/search/SearchResult.jsx');
var Category = require('../views/category/Category.jsx');
var injectTapEventPlugin = require("react-tap-event-plugin");


injectTapEventPlugin();


React.render(
	React.createElement(Category, null),
	document.getElementById('category')
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


