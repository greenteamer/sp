define(['react', 'bootstrap', 'material',], function (React) {

	var Login = React.createClass({
		render: function () {
			return (
				<div className="login-box">
				    <div className="login-logo">
				        <a href="/profile"><b>Кабинет</b> SP Moscow</a>
				    </div>
				    <div className="login-box-body">
				        <p className="login-box-msg">Войдите для начала работы</p>				       				       
				        <form method="post" action=".">
				            <div className="form-group has-feedback">
				            <input class="form-control" id="id_username" maxlength="100" name="username" placeholder="Ваше Имя" type="text"/>
				                <span className="glyphicon glyphicon-envelope form-control-feedback"></span>
				            </div>
				            <div className="form-group has-feedback">				                
				                <input class="form-control" id="id_password" name="password" placeholder="Введите пароль" type="password"/>
				                <span className="glyphicon glyphicon-lock form-control-feedback"></span>
				            </div>
				            <div className="row">
				            <div className="col-xs-12">
				                <div className="checkbox icheck">
				                    <label>
				                        <input type="checkbox"/> Запомнить меня
				                    </label>
				                </div>
				            </div>
				                <div className="col-xs-12">
				                    <button type="submit" className="btn btn-primary btn-block btn-flat">Войти</button>
				                </div>
				            </div>
				        </form>
				        <div className="social-auth-links text-center">
				            <p>- ИЛИ -</p>
				            <a href="#" className="btn btn-block btn-social btn-facebook btn-flat"><i className="fa fa-facebook"></i> Войти с помощью Facebook</a>
				            <a href="#" className="btn btn-block btn-social btn-google-plus btn-flat"><i className="fa fa-google-plus"></i> Войти с помощью Google+</a>
				        </div>
				        <a href="#">Я забыл свой пароль</a><br/>
				        <a href="/profile/registration/" className="text-center">Зарегистрироваться</a>
				    </div>
				</div>
			)
		}
	});

	React.render(<Login/>, document.getElementById('login'));

	return Login;
});