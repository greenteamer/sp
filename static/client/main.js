var React = require('react');

var App = require('./dev/views/App.jsx');
var PopularIndex = require('./dev/views/PopularIndex.jsx');
var injectTapEventPlugin = require("react-tap-event-plugin");

injectTapEventPlugin();

// React.render(
// 	React.createElement(App, null),
// 	document.getElementById('products')
// );

React.render(
	React.createElement(PopularIndex, null),
	document.getElementById('popular')
);
