var React = require('react');
var _ = require('underscore');
//material-ui
var mui = require('material-ui');
var ThemeManager = require('material-ui/lib/styles/theme-manager')();
var Slider = mui.Slider;

var PurchasesStore = require('../../stores/PurchasesStore.js');
var PurchasesActions = require('../../actions/PurchasesActions.js');

var Methods = require('../customhelpers/Methods.js');

var ReactSlider = require('react-slider');


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
    		values: [100, 1000]
    	}	
    },
    componentWillMount: function  () {
    	PurchasesStore.bind( 'change', this.collectionChanged );
    },
    collectionChanged: function () {
        // var tmp_collection = [];
        // tmp_collection.push(PurchasesStore.collection);    

        // вызываем вспомогательный метод для преобразования массива категорий в
        // простой массив продуктов (используется файл customhelpers/Methods.js)
        // tmp_filter_collection = Methods.convertCategoriesToFlatProducts(tmp_collection);
        tmp_filter_collection = Methods.convertCategoriesToFlatProducts(PurchasesStore.collection);

		this.setState({
            collection: tmp_collection,
            filtered_сollection: tmp_filter_collection
        });
    },    
    onAfterChange: function  () {
        var values = this.refs.reactSlider.getValue();
        console.log('test slider', values);
        var tmp_filtered_сollection = _.filter(this.state.filtered_сollection, function (product) {
            return product.price >= values[0] && product.price <= values[1] ;
        });
        var sorted_collection = _.sortBy(tmp_filtered_сollection, function(product){ return product.price; });
        PurchasesActions.filterCollection(sorted_collection);        
    },
    setValues: function () {
        var values = this.refs.reactSlider.getValue();
        this.setState({
            values: values
        });
    },
	render: function  () {		
		var product_max_price = _.max(this.state.filtered_сollection, function (product) {
			//получаем продукт с максимальной ценой
			return product.price;
		});
        console.log('max price: ', product_max_price);
		return (
			<div>
				<h3 className="font-decor">Фильтры</h3>            
                <ReactSlider 
                        ref="reactSlider"
                        defaultValue={[100, 1000]}
                        max={product_max_price.price+100}
                        step={100}
                        minDistance={100}
                        onAfterChange={this.onAfterChange}
                        onChange={this.setValues}
                        withBars >
                    <div className="my-handle">от: {this.state.values[0]} р.</div>
                    <div className="my-handle">до: {this.state.values[1]} р.</div>                    
                </ReactSlider>
                
			</div>
		)
	}
});


module.exports = Filters;