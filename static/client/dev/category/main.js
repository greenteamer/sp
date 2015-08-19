var React = require('react');
//var Category = require('../views/PopularIndex.jsx');
var Category = require('../views/category/Category.jsx');
var injectTapEventPlugin = require("react-tap-event-plugin");


injectTapEventPlugin();


React.render(
	React.createElement(Category, null),
	document.getElementById('category')
);
