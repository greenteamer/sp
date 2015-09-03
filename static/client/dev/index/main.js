var React = require('react');
var Router = require('react-router');
var Route = Router.Route;

//var App = require('../views/App.jsx');
var PopularIndex = require('../views/PopularIndex.jsx');
var CartMenu = require('../views/cartmenu/CartMenu.jsx');
var SearchForm = require('../views/search/SearchForm.jsx');
var SearchResult = require('../views/search/SearchResult.jsx');
var injectTapEventPlugin = require("react-tap-event-plugin");

injectTapEventPlugin();


React.render(
	React.createElement(PopularIndex, null),
	document.getElementById('popular')
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


//React.render(
//	React.createElement(SearchResult, null),
//	document.getElementById('react_fast_view_product')
//);

