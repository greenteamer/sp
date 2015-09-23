var React = require('react');
var $ = require('jquery');
var _ = require('underscore');

var QuestionList = require('./Questions.jsx');
var FaqActions = require('../actions/FaqActions.js');
var FaqStore = require('../stores/FaqStore.js');

var IF = require('../../views/customhelpers/IF.jsx');


var App = React.createClass({
	getInitialState: function () {
        return {
            questions: []
        };
    },
    
    componentDidMount: function () {                     
    },
    componentWillUnmount: function () {        
    },
    questionsChange: function () {
        // console.log('FAQ start questionsChange, FaqStore.questions: ', FaqStore.questions);
        var purchase_id = this.props.purchase.id;
        // console.log('FAQ start questionsChange purchase_id: ', purchase_id);
        tmp_questions = _.filter(FaqStore.questions, function (question) {
            return question.purchase == purchase_id;
        });
        // console.log('FAQ questionsChange tmp_questions: ', tmp_questions);
        this.setState({
            questions: tmp_questions
        });          
    },    
	render: function () {
		return (
            <IF condition={this.props.questions}>
    			<QuestionList
                    collection={this.props.questions}
                    user={this.props.user}
                    purchase={this.props.purchase}
                    product={this.props.product}
                    is_owner={this.props.is_owner} />
            </IF>
		);
	}
});

module.exports = App;