var React = require('react');
var $ = require('jquery');
var Purchases = require('../Purchases.jsx');
var PurchasesStore = require('../../stores/PurchasesStore.js');
var PurchasesActions = require('../../actions/PurchasesActions.js');
var IF = require('../customhelpers/IF.jsx');


var SearchResult = React.createClass({
	getInitialState: function () {
        return {
            search_result_collection: [],
            query_text: ''
        }
    },
    componentDidMount: function () {
        //обновляем store в соответствии с текущей категорией
        PurchasesStore.bind( 'change', this.collectionChanged );
    },
    componentWillUnmount: function () {
        PurchasesStore.unbind( 'change', this.collectionChanged );
    },
    collectionChanged: function () {
        var tmp_collection = [];
        tmp_collection.push(PurchasesStore.search_result_collection);
		this.setState({
            search_result_collection: tmp_collection,
            query_text: PurchasesStore.query_text
        });
    },
	render: function () {

        var search_result_collection = [];
		var title = 'поиск по ' + '"' + this.state.query_text + '"';
		this.state.search_result_collection.forEach(function(item){
			search_result_collection = item;
		});
        return (
            <IF condition={search_result_collection.length != 0}>
                <div className=''>            
                    <h3>{title}</h3>
                    <Purchases collection={search_result_collection}/>
                </div>
            </IF>
        )
	}
});


module.exports = SearchResult;
