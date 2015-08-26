var React = require('react');
var $ = require('jquery');
var Purchases = require('./Purchases.jsx');
var PurchasesStore = require('../stores/PurchasesStore.js');
var PromoFilter = require('./PromoFilter.jsx');
var PurchasesActions = require('../actions/PurchasesActions.js');


var PopularIndex = React.createClass({
	getInitialState: function () {
        return {
            collection: [],
          	user: {},
            title: ''
        }
    },
    componentDidMount: function () {
		PurchasesActions.getPopularPromo();
        PurchasesStore.bind( 'change', this.collectionChanged );
    },
    componentWillUnmount: function () {
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
                <h2 className="font-decor block-title">{title}</h2>
                <PromoFilter />
		    	<Purchases collection={collection} title={title}/>
            </div>
		)
	}
});


module.exports = PopularIndex;
