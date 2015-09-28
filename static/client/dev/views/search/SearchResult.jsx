var React = require('react');
var $ = require('jquery');
var _ = require('underscore');
var Purchases = require('../Purchases.jsx');
var PurchasesStore = require('../../stores/PurchasesStore.js');
var PurchasesActions = require('../../actions/PurchasesActions.js');
var IF = require('../customhelpers/IF.jsx');


var SearchResult = React.createClass({
	getInitialState: function () {
        return {
            search_result_collection: [],
            query_text: '',
            initial_purchases: [],
            result_purchases: []            
        }
    },
    componentWillMount: function () {        
        //обновляем store в соответствии с текущей категорией
        PurchasesStore.bind( 'change', this.collectionChanged );
        PurchasesStore.bind( 'getInitialPurchases', this.getPurchases );
    },    
    componentWillUnmount: function () {
        PurchasesStore.unbind( 'change', this.collectionChanged );
        PurchasesStore.unbind( 'getInitialPurchases', this.getPurchases );
    },
    collectionChanged: function () {
        // отправляем ajax и получаем все закупки 
        PurchasesActions.getInitialPurchases();

        var tmp_collection = [];
        console.log('PurchasesStore.search_result_collection : ', PurchasesStore.search_result_collection)
        tmp_collection = PurchasesStore.search_result_collection;
        
		this.setState({
            search_result_collection: tmp_collection,
            query_text: PurchasesStore.query_text            
        });
    },
    getPurchases: function () {
        console.log('get initial Purchases: ', PurchasesStore.initial_purchases);
        if (PurchasesStore.initial_purchases.length > 0) {
            var purch_id = _.pluck(this.state.search_result_collection, 'purchase_id');  
            var catal_id = _.pluck(this.state.search_result_collection, 'catalog_id');  
            var prod_id = _.pluck(this.state.search_result_collection, 'product_id');  
            console.log('purch_id : ', purch_id)

            var init_purch = PurchasesStore.initial_purchases;            
            var tmp_purch = _.filter(init_purch, function (purch) {
                return purch_id.indexOf(purch.id) != -1 ;
            });
            var new_purch = _.map(tmp_purch, function (purch) {
                purch.catalogs = _.map(
                    _.filter(purch.catalogs, function (cat) {
                        // фильтруем массив каталогов этой закупки и 
                        // оставляем в очередной закупке только наши каталоги                        
                        return catal_id.indexOf(cat.id) != -1 ;
                        // затем проходим по каждой фильтруя продукты
                    }), function (cat) {
                            // ЧИТАТЬ ОТСЮДА
                            cat.product_catalog = _.filter(cat.product_catalog, function (prod) {
                                // меняем очередной каталог так что в нем остаются только наши продукты
                                return prod_id.indexOf(prod.id) != -1;
                            });
                            return cat;
                        });
                return purch;                
            });
            console.log('tmp_purch : ', tmp_purch);
            console.log('new_purch', new_purch);
            // console.log('tmp_catal : ', tmp_catal)
            // _.each(tmp_purch, function (purch) {
                
            // });
        };

        this.setState({
            initial_purchases: PurchasesStore.initial_purchases,
            result_purchases: new_purch
        });
    },
	render: function () {
        console.log('search render this.state.result_purchases: ', this.state.result_purchases);
        // var search_result_collection = [];
		var title = 'поиск по ' + '"' + this.state.query_text + '"';
		// this.state.search_result_collection.forEach(function(item){
		// 	search_result_collection = item;
		// });
        return (
            <IF condition={this.state.result_purchases.length != 0}>
                <div className=''>            
                    <h3>{title}</h3>
                    <Purchases collection={this.state.result_purchases}/>
                </div>
            </IF>
        )
	}
});


module.exports = SearchResult;
