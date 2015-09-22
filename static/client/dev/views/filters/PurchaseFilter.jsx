var React = require('react');
var _ = require('underscore');
//material-ui
var mui = require('material-ui');
var ThemeManager = require('material-ui/lib/styles/theme-manager')();
var Slider = mui.Slider;

var PurchasesStore = require('../../stores/PurchasesStore.js');
var PurchasesActions = require('../../actions/PurchasesActions.js');

var Methods = require('../customhelpers/Methods.js');
var IF = require('../customhelpers/IF.jsx');
var FiltFunc = require('../customhelpers/FilterFunctions.js');

var ReactSlider = require('react-slider');


var CategoryFilter = React.createClass({
    getInitialState: function () {
        return {
            collection: [],
            categories: [],
            nested_categories: []
        };
    },
    componentWillMount: function () {        
        PurchasesActions.getCategoriesTree();
        PurchasesStore.bind('categoryReceived', this.setChildrenCategory);
        PurchasesStore.bind( 'change', this.collectionChanged );
    },
    componentWillUnmount: function () {                
        PurchasesStore.unbind('categoryReceived', this.setChildrenCategory);
        PurchasesStore.unbind( 'change', this.collectionChanged );
    },
    collectionChanged: function () {        
        this.setState({
            collection: PurchasesStore.collection
        });
    },
    setChildrenCategory: function () {
                    
        // получаем все вложенные категории этой категории       
        console.log('initial data PurchasesStore.collection: ', PurchasesStore.collection);
        console.log('initial data PurchasesStore.collection[0].catalogs: ', PurchasesStore.collection[0].catalogs);
        console.log('initial data PurchasesStore.categories: ', PurchasesStore.categories);
        var tmp_nested_categories = []; 
        _.each(PurchasesStore.collection[0].catalogs, function (catalog) {
            _.each(PurchasesStore.categories, function (category) {                
                if (catalog.categories[0] == category.id) {
                    console.log('catalog.categories in map: ', catalog.categories[0]);
                    console.log('category in all categories: ', category.id);
                    tmp_nested_categories.push(category);
                };                
            });
        });
        console.log('tmp_nested_categories', tmp_nested_categories);
        this.setState({
            categories: PurchasesStore.categories,
            nested_categories: tmp_nested_categories
        });          
    },
    changeCategoryFilter: function (e) {
        console.log('cat filter: ', e.target.id);
        var category_slug = e.target.id;          
        PurchasesActions.filterByCategory(category_slug);      
    },     
    render: function () {
        // биндим функцию что бы она была доступна внутри map        
        var bindFun = this.changeCategoryFilter;

        var nested_categories = this.state.nested_categories.map(function (tmp_cat) {
            // генерируем кнопки с фильтрами
            var link = "/category-" + tmp_cat.slug;
            return (
                <button onClick={bindFun} id={tmp_cat.slug} className="btn btn-primary">                    
                    {tmp_cat.name}
                </button>
            );
        });
        return (
            <div>
                <IF condition={this.state.nested_categories.length > 0}>
                    <div> 
                        <h3 className="font-decor">Фильтры по категориям</h3>
                        {nested_categories}
                    </div>
                </IF>
            </div>
        );
    }
});


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
        // values - для отслеживания изменений бегунков и отрисовки их текущих значений
        // flat_collection - создаем из сложной коллекции категорий массив продуктов для фильтрации
        // filtered_сollection - отфильтрованный результат (используется другими фильтрами)
    	return {
    		flat_collection: [],
    		filtered_сollection: [],
    		values: []
    	};
    },
    componentWillMount: function  () {
    	PurchasesStore.bind( 'change', this.collectionChanged );
    },
    componentWillUnmount: function () {
        PurchasesStore.unbind( 'change', this.collectionChanged );
    },
    collectionChanged: function () { 
        // УСТАНАВЛИВАЕМ ЗНАЧЕНИЯ СОСТОЯНИЯ КОМПОНЕНТА
        // вызываем вспомогательный метод для преобразования массива категорий в
        // простой массив продуктов (используется файл customhelpers/Methods.js)
        // метод вызывается только когда меняется основная коллекция, скорее всего это перезагрузка страницы
        // flat_сollection - создаем примитивизированный вариант основной коллекции collection
        console.log('filter for purchase PurchasesStore.collection:', PurchasesStore.collection);
        flat_purchases_collection = Methods.convertPurchasesToFlatProducts(PurchasesStore.collection);
        var product_max_price = _.max(flat_purchases_collection, function (product) {
            //получаем продукт с максимальной ценой
            return product.price;
        });
        PurchasesActions.filterByPrice([0, product_max_price.price + 100]);
		this.setState({
            flat_collection: flat_purchases_collection,
            filtered_сollection: flat_purchases_collection,
            values: [0, product_max_price.price + 100]
        });
    },        
    onAfterChange: function () {
        var values = this.refs.reactSlider.getValue();
        console.log('onAfterChange function : ', values);
        PurchasesActions.filterByPrice(values);
    },
    setValues: function () {
        // МЕНЯЕМ ЗАНЧЕНИЯ БЕГУНКОВ СЛАЙДЕРА НА АКТУАЛЬНЫЕ
        var values = this.refs.reactSlider.getValue();
        this.setState({
            values: values
        });
    },
	render: function  () {		
		var product_max_price = _.max(this.state.flat_collection, function (product) {
			//получаем продукт с максимальной ценой
			return product.price;
		});     
		return (            
			<div>
				<h3 className="font-decor">Фильтры</h3>            
                <ReactSlider 
                        ref="reactSlider"                        
                        defaultValue={[0, 1000]}                        
                        max={product_max_price.price+100}
                        step={100}
                        minDistance={100}
                        onAfterChange={this.onAfterChange}
                        onChange={this.setValues}
                        withBars >
                    <div className="my-handle">от: {this.state.values[0]} р.</div>
                    <div className="my-handle">до: {this.state.values[1]} р.</div>                    
                </ReactSlider>

                <CategoryFilter />                
			</div>
		);
	}
});


module.exports = Filters;