define(['react', 'bootstrap', 'material',], function (React) {

	var Login = React.createClass({displayName: "Login",
		render: function () {
			return (
				React.createElement("div", {className: "login-box"}, 
				    React.createElement("div", {className: "login-logo"}, 
				        React.createElement("a", {href: "/profile"}, React.createElement("b", null, "Кабинет"), " SP Moscow")
				    ), 
				    React.createElement("div", {className: "login-box-body"}, 
				        React.createElement("p", {className: "login-box-msg"}, "Войдите для начала работы"), 				       				       
				        React.createElement("form", {method: "post", action: "."}, 
				            React.createElement("div", {className: "form-group has-feedback"}, 
				                React.createElement("input", {class: "form-control empty", id: "focusedInput", maxlength: "100", name: "username", type: "text"}), 
				                React.createElement("span", {className: "glyphicon glyphicon-envelope form-control-feedback"})
				            ), 
				            React.createElement("div", {className: "form-group has-feedback"}, 
				                React.createElement("input", {class: "form-control empty", id: "id_password1", name: "password1", type: "password"}), 
				                React.createElement("span", {className: "glyphicon glyphicon-lock form-control-feedback"})
				            ), 
				            React.createElement("div", {className: "row"}, 
				            React.createElement("div", {className: "col-xs-12"}, 
				                React.createElement("div", {className: "checkbox icheck"}, 
				                    React.createElement("label", null, 
				                        React.createElement("input", {type: "checkbox"}), " Запомнить меня"
				                    )
				                )
				            ), 
				                React.createElement("div", {className: "col-xs-12"}, 
				                    React.createElement("button", {type: "submit", className: "btn btn-primary btn-block btn-flat"}, "Войти")
				                )
				            )
				        ), 
				        React.createElement("div", {className: "social-auth-links text-center"}, 
				            React.createElement("p", null, "- ИЛИ -"), 
				            React.createElement("a", {href: "#", className: "btn btn-block btn-social btn-facebook btn-flat"}, React.createElement("i", {className: "fa fa-facebook"}), " Войти с помощью Facebook"), 
				            React.createElement("a", {href: "#", className: "btn btn-block btn-social btn-google-plus btn-flat"}, React.createElement("i", {className: "fa fa-google-plus"}), " Войти с помощью Google+")
				        ), 
				        React.createElement("a", {href: "#"}, "Я забыл свой пароль"), React.createElement("br", null), 
				        React.createElement("a", {href: "/profile/registration/", className: "text-center"}, "Зарегистрироваться")
				    )
				)
			)
		}
	});

	React.render(React.createElement(Login, null), document.getElementById('login'));

	return Login;
});