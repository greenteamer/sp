var React = require('react');
var $ = require('jquery');
var _ = require('underscore');

var QuestionList = require('./Questions.jsx');
var FaqActions = require('../actions/FaqActions.js');
var FaqStore = require('../stores/FaqStore.js');


var App = React.createClass({
	getInitialState: function () {
        return {
            collection: []
        };
    },
    
    componentDidMount: function () {       
        FaqActions.getFaqTree();        
        FaqStore.bind( 'change', this.collectionChanged );            
    },
    componentWillUnmount: function () {
        FaqStore.unbind( 'change', this.collectionChanged );        
    },
    collectionChanged: function () {
        var purchase_id = this.props.purchase.id;
        tmp_collection = _.filter(FaqStore.collection, function (question) {
            return question.purchase == purchase_id;
        });
        this.setState({
            collection: tmp_collection
        });          
    },    
	render: function () {		
		return (
			<QuestionList
                collection={this.state.collection}
                user={this.props.user}
                purchase={this.props.purchase}
                product={this.props.product}
                is_owner={this.props.is_owner} />
		);
	}
});

module.exports = App;