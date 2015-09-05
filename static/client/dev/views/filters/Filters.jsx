var React = require('react');
var _ = require('underscore');
//material-ui
var mui = require('material-ui');
var ThemeManager = require('material-ui/lib/styles/theme-manager')();
var Slider = mui.Slider;

var PurchasesStore = require('../../stores/PurchasesStore.js');
var PurchasesActions = require('../../actions/PurchasesActions.js');

var Methods = require('../customhelpers/Methods.js');


var Filters = React.createClass({
	childContextTypes: {
        muiTheme: React.PropTypes.object
    },
    getChildContext: function() {
        return {
            muiTheme: ThemeManager.getCurrentTheme()
        };
    },
    getInitialState: function  () {
    	return {
    		collection: [],
    		filtered_сollection: [],
    		value: 0
    	}	
    },
    componentWillMount: function  () {
    	PurchasesStore.bind( 'change', this.collectionChanged );
    },
    collectionChanged: function () {
        var tmp_collection = [];
        tmp_collection.push(PurchasesStore.collection);    

        // вызываем вспомогательный метод для преобразования массива категорий в
        // простой массив продуктов (используется файл customhelpers/Methods.js)
        tmp_filter_collection = Methods.convertCategoriesToFlatProducts(tmp_collection);

		this.setState({
            collection: tmp_collection,
            filtered_сollection: tmp_filter_collection            
        });        
    },
    changeValue: function (e, value) {        
        var tmp_filtered_сollection = _.filter(this.state.filtered_сollection, function (product) {
            return product.price <= value;
        });
        var sorted_collection = _.sortBy(tmp_filtered_сollection, function(product){ return product.price; });
        console.log('sorted_collection', sorted_collection);
    	this.setState({
    		value: value            
    	});
    	PurchasesActions.filterCollection(sorted_collection);
    },
	render: function  () {
		console.log('collection: ', this.state.collection);
		console.log('filter collection: ', this.state.filtered_сollection);
	
		var product_max_price = _.max(this.state.filtered_сollection, function (product) {
			//получаем продукт с максимальной ценой
			return product.price;
		});		
		return (
			<div>
				<h3 className="font-decor">Фильтры</h3>
				<p className="price">Цена до {this.state.value} р.</p>	
				<Slider
					name="price_slider"
					onChange={this.changeValue}                    
					defaultValue={0}
					max={product_max_price.price}
					step={100} />
			</div>
		)
	}
});


module.exports = Filters;