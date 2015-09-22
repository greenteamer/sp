var React = require('react');
var $ = require('jquery');
var _ = require('underscore');

var QuestionList = require('./Questions.jsx');
var FaqActions = require('../actions/FaqActions.js');
var FaqStore = require('../stores/FaqStore.js');


var App = React.createClass({
	getInitialState: function () {
        return {
            questions: []
        };
    },
    
    componentDidMount: function () {       
        FaqActions.getFaqTree();        
        FaqStore.bind( 'questionsChange', this.questionsChange );            
    },
    componentWillUnmount: function () {
        FaqStore.unbind( 'questionsChange', this.questionsChange );        
    },
    questionsChange: function () {
        var purchase_id = this.props.purchase.id;
        tmp_questions = _.filter(FaqStore.questions, function (question) {
            return question.purchase == purchase_id;
        });
        this.setState({
            questions: tmp_questions
        });          
    },    
	render: function () {
		return (
			<QuestionList
                collection={this.state.questions}
                user={this.props.user}
                purchase={this.props.purchase}
                product={this.props.product}
                is_owner={this.props.is_owner} />
		);
	}
});

module.exports = App;