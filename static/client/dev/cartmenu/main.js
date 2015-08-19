var React = require('react');
var CartMenu = require('../views/cartmenu/CartMenu.jsx');
var injectTapEventPlugin = require("react-tap-event-plugin");


injectTapEventPlugin();


React.render(
	React.createElement(CartMenu, null),
	document.getElementById('cartmenu')
);
