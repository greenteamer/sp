var React = require('react');

var FlatButton = require('material-ui').FlatButton;
var Dialog = require('material-ui').Dialog;
var Checkbox = require('material-ui').Checkbox;
var ThemeManager = require('material-ui/lib/styles/theme-manager')();
var injectTapEventPlugin = require("react-tap-event-plugin");

var AnswerList = require('./Answers.jsx');
var AnswerModal = require('./AnswerModal.jsx');
var QuestionModal = require('./QuestionModal.jsx');
var FaqActions = require('../actions/FaqActions.js');

var IF  = require('../../views/customhelpers/IF.jsx');


var Question = React.createClass({
	childContextTypes: {
        muiTheme: React.PropTypes.object
    },
    getChildContext: function() {        
        return {
            muiTheme: ThemeManager.getCurrentTheme()
        };
    },
    question_checked: function () {    	
    	FaqActions.question_checked({
    		id: this.props.question.id,
    		status: this.refs.checked_ref.isChecked()
    	});
    },
	render: function () {
		var checker = <Checkbox
	        name="checkboxName2"
	        ref="checked_ref"
	        style={{ width: '100%', margin: '0 auto'}}
	        label="Опубликовано"
	        defaultChecked={this.props.question.checked}
	        onCheck={this.question_checked} />;
        var text = this.props.question.text;
        function createDescription() { 
            return {__html: text }; 
        };
		return (
			<div className="col-xs-12">
				<div className="question-faq">					
					<h2 ref="title_question">{this.props.question.title} <span className="small question-date">{this.props.question.date}</span></h2>
					<IF condition={true}>
						<div ref="text_question" dangerouslySetInnerHTML={createDescription()} />
					</IF>
					<IF condition={false}>
						<div>
							{checker}							
							<div ref="text_question" dangerouslySetInnerHTML={createDescription()} />								
							<AnswerModal id={this.props.question.id} user={this.props.user} />
						</div>
					</IF>
				</div>
				<div className="answers">					
					<AnswerList answers={this.props.question.answers} />
				</div>
			</div>
		);				
	}
});


var QuestionList = React.createClass({
	render: function () {
		var user = this.props.user;
		var is_owner = this.props.is_owner;
		items = this.props.collection.map(function (item){
			return (
				<Question question={item} user={user} is_owner={is_owner}/>
			);
		});
		return (			
			<div className="row">				
				<QuestionModal 
					purchase={this.props.purchase} 
					product={this.props.product} 
					user={this.props.user}/>
				{items}
			</div>
		);
	}
});


module.exports = QuestionList;