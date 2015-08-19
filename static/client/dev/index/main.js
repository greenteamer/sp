var React = require('react');

var App = require('../views/App.jsx');
var PopularIndex = require('../views/PopularIndex.jsx');
var injectTapEventPlugin = require("react-tap-event-plugin");

injectTapEventPlugin();


React.render(
	React.createElement(PopularIndex, null),
	document.getElementById('popular')
);
