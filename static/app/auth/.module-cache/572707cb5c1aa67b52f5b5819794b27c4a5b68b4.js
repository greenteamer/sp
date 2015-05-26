define(['react', 'bootstrap', 'cookie',]), function (React) {

	Login = React.createClass({displayName: "Login",
		render: function () {
			return (React.createElement("div", {className: "login-box"}, 
						React.createElement("h1", null, "Hello!")				
					))
		}
	});

	React.render(React.createElement(Login, null), getElementById('login'));

	return Login;
}