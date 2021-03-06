var React = require('react');
var $ = require('jquery');
var Purchases = require('../Purchases.jsx');
var PurchasesStore = require('../../stores/PurchasesStore.js');
var PurchasesActions = require('../../actions/PurchasesActions.js');


var Search = React.createClass({
	getInitialState: function () {
        return {
            cartitems: []
        }
    },
    componentWillMount: function(){
        //PurchasesActions.getCartItems();
    },
    componentDidMount: function () {
        //обновляем store в соответствии с текущей категорией
        //PurchasesActions.getCartItems();
        //PurchasesStore.bind( 'change', this.collectionChanged );
    },
    componentWillUnmount: function () {
        //PurchasesStore.unbind( 'change', this.collectionChanged );
    },
    collectionChanged: function () {
		this.setState({
            cartitems: PurchasesStore.cartitems
        });
    },
    search: function(e){
        var query = React.findDOMNode(this.refs.query_text).value;
        PurchasesActions.getSearchResults(query);
        e.preventDefault();
    },
	render: function () {
		return (
            <form className="custom-form" onSubmit={this.search}>
                <input type="text" ref="query_text" className="col-lg-8" placeholder="поиск товаров"/>
                <button type="submit" className="btn btn-primary pull-left btn-search">
                    <i className="mdi-action-search"></i>
                </button>
            </form>
		)
	}
});


module.exports = Search;
