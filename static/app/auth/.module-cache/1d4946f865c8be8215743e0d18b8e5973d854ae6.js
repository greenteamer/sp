define(['react',], function (React) {

	var Login = React.createClass({displayName: "Login",
		render: function () {
			return (
				React.createElement("div", {className: "login-box"}, 
					React.createElement("h1", null, "Hello, Aleks!")				
				)
			)
		}
	});

	React.render(React.createElement(Login, null), document.getElementById('login'));

	return Login;
});