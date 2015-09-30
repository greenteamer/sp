var React = require('react');
var $ = require('jquery');
var _ = require('underscore');
var Purchases = require('../Purchases.jsx');
var PurchasesStore = require('../../stores/PurchasesStore.js');
var SearchStore = require('../../stores/SearchStore.js');
var PurchasesActions = require('../../actions/PurchasesActions.js');

var IF = require('../customhelpers/IF.jsx');
var SearchFunctions = require('../customhelpers/SearchFunctions.js');

var SearchResult = React.createClass({
	getInitialState: function () {
        return {
            query: '',
            result_purchases: []            
        };
    },
    componentWillMount: function () {               
        //обновляем store в соответствии с текущей категорией
        SearchStore.bind('searchStateTrigger', this.searchStateTrigger);
        PurchasesStore.bind( 'getInitialPurchases', this.getAllPurchases );
        PurchasesStore.bind('categoryReceived', this.categoryReceived);
        PurchasesStore.bind('catalogsReceived', this.catalogsReceived);
    },    
    componentWillUnmount: function () {
        SearchStore.unbind('searchStateTrigger', this.searchStateTrigger);
        PurchasesStore.unbind( 'getInitialPurchases', this.getAllPurchases );
        PurchasesStore.unbind('catalogsReceived', this.catalogsReceived);
    },
    searchStateTrigger: function(){
        console.log('SearchResult searchStateTrigger start', SearchStore.search.search_state.query);

        setTimeout(function() {
            PurchasesActions.getCatalogs(); 
        }, 10);
        
        this.setState({
            search: SearchStore.search
        });
    },
    categoryReceived: function () {
        console.log('SearchResult categoryReceived done: ', PurchasesStore.categories);
        // PurchasesActions.getInitialPurchases();
    },
    catalogsReceived: function  () {
        setTimeout(function() {
            PurchasesActions.getInitialPurchases(); 
        }, 10);
    },
    getAllPurchases: function () {
        var result = SearchFunctions.search(
                        PurchasesStore.initial_purchases, 
                        PurchasesStore.categories, 
                        PurchasesStore.catalogs, 
                        SearchStore.search);
        console.log('SearchResult jsx getAllPurchases search result: ', result);

        this.setState({
            query: SearchStore.search.search_state.query,
            result_purchases: result
        });
    },
	render: function () {
        console.log('search render this.state.result_purchases: ', this.state.result_purchases);
		var title = 'поиск по ' + '"' + this.state.query + '"';
        return (
            <IF condition={this.state.result_purchases.length != 0}>
                <div className=''>            
                    <h3>{title}</h3>
                    <Purchases collection={this.state.result_purchases}/>
                </div>
            </IF>
        );
	}
});


module.exports = SearchResult;
