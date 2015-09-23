var React = require('react');
//var Category = require('../views/PopularIndex.jsx');
var CartMenu = require('../views/cartmenu/CartMenu.jsx');
var SearchForm = require('../views/search/SearchForm.jsx');
var SearchResult = require('../views/search/SearchResult.jsx');
var Product = require('../views/product/Product.jsx');
var Breadcrumbs = require('../views/breadcrumbs/Breadcrumbs.jsx');
var injectTapEventPlugin = require("react-tap-event-plugin");


injectTapEventPlugin();


React.render(
	<Product />,
	document.getElementById('product')
);

React.render(
	<Breadcrumbs/>,
	document.getElementById('breadcrumbs')
);

React.render(
	<CartMenu/>,
	document.getElementById('cartmenu')
);


React.render(
	<SearchForm/>,
	document.getElementById('react_search')
);


React.render(
	<SearchResult/>,
	document.getElementById('react_search_result')
);

