var React = require('react');
var $ = require('jquery');
var Purchases = require('./Purchases.jsx');
var PurchasesStore = require('../stores/PurchasesStore.js');

// actions
var PurchasesActions = require('../actions/PurchasesActions.js');


var PopularIndex = React.createClass({
	getInitialState: function () {
        return {
            collection: [],
          	user: {}
        }
    },
    componentDidMount: function () {
		PurchasesActions.getPopularPromo();
        PurchasesStore.bind( 'change', this.collectionChanged );
        console.log('component did mount');
    },
    componentWillUnmount: function () {
        console.log('component will unmount');
        PurchasesStore.unbind( 'change', this.collectionChanged );
    },
    collectionChanged: function () {
		this.setState({
            collection: PurchasesStore.collection
        });
    },
	render: function () {
		collection = [];
		var title = '';
		this.state.collection.forEach(function(item){
			collection = item.promo_purchase;
			title = item.name;
		});
		return (
            <div>
		    	<Purchases collection={collection} title={title}/>
            </div>
		)
	}
});


module.exports = PopularIndex;
