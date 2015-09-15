var React = require('react');
var _ = require('underscore');
//material-ui
var mui = require('material-ui');
var ThemeManager = require('material-ui/lib/styles/theme-manager')();
var Slider = mui.Slider;

var PurchasesStore = require('../../stores/PurchasesStore.js');
var PurchasesActions = require('../../actions/PurchasesActions.js');

var Methods = require('../customhelpers/Methods.js');
var FiltFunc = require('../customhelpers/FilterFunctions.js');

var ReactSlider = require('react-slider');


var CategoryFilter = React.createClass({
    getInitialState: function () {
        return {
            categories: [],
            nested_categories: []
        };
    },
    componentWillMount: function () {        
        PurchasesActions.getCategoriesTree();
        PurchasesStore.bind('categoryReceived', this.setChildrenCategory);
    },
    componentWillUnmount: function () {                
        PurchasesStore.unbind('categoryReceived', this.setChildrenCategory);
    },
    setChildrenCategory: function () {
        // получаем slug категории по url      
        var current_category_slug = Methods.getCategorySlug();        

        // получаем все вложенные категории этой категории
        tmp_nested_categories = Methods.getAllNestedCategories(PurchasesStore.categories, current_category_slug);
        this.setState({
            categories: PurchasesStore.categories,
            nested_categories: tmp_nested_categories
        });  
    },
    changeCategoryFilter: function (e) {
        console.log('cat filter: ', e.target.id);
        var category_slug = e.target.id;          
        PurchasesActions.filterByCategory(category_slug);
        // var category_slug = e.target.id;
        // var category = _.find(this.state.nested_categories, function (cat) {
        //     return cat.slug == category_slug;
        // });

        // var cat_purchases = Methods.getPurchasesFromCategories(this.state.categories, category_slug);

        // var tmp_filtered_collection = FiltFunc.filterByCategory(cat_purchases, this.props.filtered_сollection);

        // PurchasesActions.filterCollection(tmp_filtered_collection);        
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
                <h3 className="font-decor">Фильтры по категориям</h3>
                {nested_categories}
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
    		values: [],
            // max_price: 0
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
        flat_purchases_collection = Methods.convertCategoriesToFlatProducts(PurchasesStore.collection);
        var product_max_price = _.max(flat_purchases_collection, function (product) {
            //получаем продукт с максимальной ценой
            return product.price;
        });
        PurchasesActions.filterByPrice([0, product_max_price.price + 100]);
		this.setState({
            flat_collection: flat_purchases_collection,
            filtered_сollection: flat_purchases_collection,
            values: [0, product_max_price.price + 100]
            // max_price: product_max_price.price + 100
        });
    },    
    onAfterChange: function  () {
        // МЕНЯЕМ КОЛЛЕКЦИЮ ПОСЛЕ ТОГО КАК ИЗМЕНИТСЯ ДИАПАЗОН ЦЕН
        var values = this.refs.reactSlider.getValue();        

        var tmp_filtered_collection = FiltFunc.filterByPrice(this.state.flat_collection, values);
        PurchasesActions.filterCollection(tmp_filtered_collection);
        // записываем в состояние компонента промежуточный результат фильтра
        this.setState({
            filtered_сollection: tmp_filtered_collection
        });      
    }, 
    onAfterChange2: function () {
        var values = this.refs.reactSlider.getValue();        
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
                        onAfterChange={this.onAfterChange2}
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