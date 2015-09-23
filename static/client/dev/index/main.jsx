var React = require('react');

var Router = require('react-router');
var Route = Router.Route;
var RouteHandler = Router.RouteHandler;

// var ReactRouter = require('react-router');
// var Router = ReactRouter.Router;
// var Route = ReactRouter.Route;
// var Link = ReactRouter.Link;
// var History = require('react-router/lib/History.js');

//var App = require('../views/App.jsx');
var PopularIndex = require('../views/PopularIndex.jsx');
var CartMenu = require('../views/cartmenu/CartMenu.jsx');
var Cart = require('../views/cartmenu/Cart.jsx');
var Breadcrumbs = require('../views/breadcrumbs/Breadcrumbs.jsx');
var SearchForm = require('../views/search/SearchForm.jsx');
var SearchResult = require('../views/search/SearchResult.jsx');
var injectTapEventPlugin = require("react-tap-event-plugin");

injectTapEventPlugin();


var About = React.createClass({	
	getInitialState: function  () {
		return {
			message: ''
		};
	},
	render: function(){
		console.log('message: ', this.props.params.id);	
		return (
			<div>
				<p>типа страничка о нас</p>
			</div>
		);
	
	}
});


var Message = React.createClass({		
	render: function  () {
		return (
			<div>
				<h4>Message</h4>
			</div>
		);
	}
});


var Company = React.createClass({
	render: function  () {
		return (
			<div>
				<h3>This is the nested url Company</h3>
			</div>
		);
	}
});


var App = React.createClass({
  	render: function() {
	    return (
	      	<div>
		        <RouteHandler/>
	      	</div>
	    );
  	}
});


var routes = (
  	<Route path="/" handler={App}>
  		<Route path="/popular" handler={PopularIndex}/>
  		<Route path="/cart" handler={Cart}/>
  	</Route>
);



// для react-router
// Router.run(routes, Router.HashLocation, function(Root){
//   React.render(<Root/>, document.getElementById('popular'));
// });


React.render(<PopularIndex />, document.getElementById('popular'));
React.render(<Breadcrumbs />, document.getElementById('breadcrumbs'));
React.render(<CartMenu />, document.getElementById('cartmenu'));
React.render(<SearchForm />, document.getElementById('react_search'));
React.render(<SearchResult />, document.getElementById('react_search_result'));
