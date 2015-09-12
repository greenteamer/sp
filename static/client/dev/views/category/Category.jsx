var React = require('react');
var $ = require('jquery');
var Purchases = require('../Purchases.jsx');
var PurchasesStore = require('../../stores/PurchasesStore.js');
var PurchasesActions = require('../../actions/PurchasesActions.js');
var ProductRelativeTitle = require('../product_components/ProductRelativeTitle.jsx');
var ProductModal = require('../product_components/ProductModal.jsx');

var IF = require('../customhelpers/IF.jsx');


var Category = React.createClass({
	getInitialState: function () {
        return {
            collection: [],
            filtered_collection: [],
          	user: {}            
        }
    },
    componentDidMount: function () {
        // устанавливаем view_state.view_page как category
        PurchasesActions.setViewPage('category');
        PurchasesActions.viewBy('products');
        //получаем текущий урл
        var url = $(location).attr('pathname');
        var parse_url = url.split('/')[1];        
        var current_category = parse_url.slice(9);
        console.log("category url :", url, parse_url, current_category);

        //обновляем store в соответствии с текущей категорией
		PurchasesActions.getCategoryPurchases(current_category);
        PurchasesStore.bind( 'change', this.collectionChanged );
        PurchasesStore.bind( 'filterTrigger', this.filterTrigger );
    },
    componentWillUnmount: function () {
        PurchasesStore.unbind( 'change', this.collectionChanged );
    },
    collectionChanged: function () {
  //       var tmp_collection = [];
  //       tmp_collection.push(PurchasesStore.collection);
		// this.setState({
  //           collection: tmp_collection
  //       });        
        this.setState({
            collection: PurchasesStore.collection
        });
    },
    filterTrigger: function () {
        this.setState({
            filtered_collection: PurchasesStore.filter.filtered_collection
        });
    },
	render: function () {
        collection = [];        
		var title = '';
        var category_id = 0;
		this.state.collection.forEach(function(item){
			collection = item.category_purchase;
			title = item.name;
            category_id = item.id;
		}); 

        var filtered_items = []; 
        if (this.state.filtered_collection.length != 0){
            filtered_items = this.state.filtered_collection.map(function (product) {
                return (
                    <div className="col-xs-12 col-sm-4 col-md-3 col-lg-3">
                        <ProductRelativeTitle product={product}/>
                    </div>
                )
            });
        }      
		return (            
            <div>
                <IF condition={this.state.filtered_collection.length == 0}>
                    <Purchases 
                        collection={this.state.collection}
                        category_id={category_id}
                        title={title}
                        indicatorElementName='#category'/>
                </IF>
                <IF condition={this.state.filtered_collection.length != 0}>
                    <div>
                        {filtered_items}
                        <ProductModal />
                    </div>                    
                </IF>                
            </div>
		)
	}
});


module.exports = Category;
