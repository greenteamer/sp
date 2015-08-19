var React = require('react');
var $ = require('jquery');
var Purchases = require('../Purchases.jsx');
var PurchasesStore = require('../../stores/PurchasesStore.js');

// actions
var PurchasesActions = require('../../actions/PurchasesActions.js');


var PopularIndex = React.createClass({
	getInitialState: function () {
        return {
            collection: [],
          	user: {}
        }
    },
    componentDidMount: function () {
        //получаем текущий урл
        var url = $(location).attr('pathname');
        var parse_url = url.split('/')[2];
        var current_category = parse_url.slice(9);
        console.log(current_category);

        //обновляем store в соответствии с текущей категорией
		PurchasesActions.getCategoryPurchases(current_category);
        PurchasesStore.bind( 'change', this.collectionChanged );
    },
    componentWillUnmount: function () {
        PurchasesStore.unbind( 'change', this.collectionChanged );
    },
    collectionChanged: function () {
        var tmp_collection = [];
        tmp_collection.push(PurchasesStore.collection);
		this.setState({
            collection: tmp_collection
        });
    },
	render: function () {
        collection = [];
		var title = '';
		this.state.collection.forEach(function(item){
			collection = item.category_purchase;
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
