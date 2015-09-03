var React = require('react');
var TestView = require('./TestView.jsx');

React.render(
	React.createElement(TestView, null),
	document.getElementById('test')
);