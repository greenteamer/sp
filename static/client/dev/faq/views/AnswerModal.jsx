var React = require('react');

var FlatButton = require('material-ui').FlatButton;
var Dialog = require('material-ui').Dialog;
var TextField = require('material-ui').TextField;
var ThemeManager = require('material-ui/lib/styles/theme-manager')();
var injectTapEventPlugin = require("react-tap-event-plugin");

var FaqActions = require('../actions/FaqActions.js');


var AnswerModal = React.createClass({
	getInitialState: function () {
	    return {
	        modal: true  
	    };
	},
    childContextTypes: {
        muiTheme: React.PropTypes.object
    },
    getChildContext: function() {        
        return {
            muiTheme: ThemeManager.getCurrentTheme()
        };
    },
    _showModal: function () {
    	this.refs.answerDialog.show();
    },    
    _DialogCancel: function () {
    	this.refs.answerDialog.dismiss();
    },
    _DialogSubmit: function (e) {
    	e.preventDefault();
    	console.log(this.refs.text_ref.getValue());
        FaqActions.answer({
        	id: this.props.id,
            text: this.refs.text_ref.getValue()
        });
        this.refs.answerDialog.dismiss();
    },
    render: function () {
    	var answerActions = [
			  <FlatButton
			    label="Закрыть"				    
			    secondary={true}
			    className="modal-button-cancel"
			    onClick={this._DialogCancel} />,
			  <FlatButton
			    label="Ответить"
			    primary={true}
			    className="modal-button-ok"
			    onClick={this._DialogSubmit} />
			];
		var modalForm = [														
				<TextField
				  ref="text_ref"
				  hintText="Ваш вопрос"
				  style={{width: '100%', margin: '0 auto'}}
				  multiLine={true}
				  floatingLabelText="Введите текст (поле ввода расширяется автоматически)"/>
			];					
		var modalAnswer = [
			<Dialog
              ref="answerDialog"
			  title="Ответить на вопрос"
			  actions={answerActions}
			  modal={this.state.modal}>
			  {modalForm}
			</Dialog>	
			];
		var classString = 'btn btn-primary';
		if (this.props.user.is_servant === false) {
			classString += ' hide';
		};
        return (				
            	<div>
            		<div className="text-right">					
						<button onClick={this._showModal} ref="answer_ref" className={classString}>Ответить</button>
					</div>
					{modalAnswer}
				</div>
        )        
    }
});


module.exports = AnswerModal;