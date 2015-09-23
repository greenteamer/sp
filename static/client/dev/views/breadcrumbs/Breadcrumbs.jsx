var React = require('react');
var _ = require('underscore');

var PurchasesStore = require('../../stores/PurchasesStore.js');
var PurchasesActions = require('../../actions/PurchasesActions.js');


function getCatTree (categories, current_category_slug) {
	// вначаел всегда главная страница
	var tree = [
		{
			'name': 'Главная',
			'href': '/'
		}		
	];

	// получаем текущую категорию
	var current_cat = _.find(categories, function  (cat) {
		return cat.slug == current_category_slug;
	});
	// если это вложенна категория находим родительскую категорию
	if (current_cat.parent != null) {
		var parent_cat = _.find(categories, function (cat) {
			return cat.id == current_cat.parent;
		});
		// родительская категория тоже имеет родителя - находим его
		if (parent_cat.parent != null) {			
			var first_parent_cat = _.find(categories, function (cat) {
				return cat.id == parent_cat.parent;
			});
			tree.push({
				// добавляем самую родительскую категорию в первую очередь
				'name': first_parent_cat.name,
				'href': '/category-' + first_parent_cat.slug
			});			
		};
		tree.push({
			// добавляем родительскую категорию
			'name': parent_cat.name,
			'href': '/category-' + parent_cat.slug
		});
	};
	tree.push({
		// добавляем родительскую категорию
		'name': current_cat.name,
		'href': '/category-' + current_cat.slug
	});
	return tree;
}


function getProdTree(categories, product){
	var tree = [
		{
			'name': 'Главная',
			'href': '/'
		}
	];
	// находим закупку
	_.each(categories, function (cat) {
		_.each(cat.category_purchase, function (purch) {
			var current_purch = _.some(purch.catalogs, function (catalog) {
				return catalog.id == product.catalog_obj.id;
			});
			if (current_purch) {				
				tree.push({
					'name': purch.name,
					'href': '/purchases/' + purch.id + '/'
				});
			};
		}); 
	});
	// удаляем повторяющиеся ссылки на закупки из массива
	tree = _.uniq(tree, function (link) {
		return link.name;
	});
	// добавляем сам товар вконце
	tree.push({
		'name': product.product_name,
		'href': '/products/' + product.id + '/'
	});
	return tree;
}


var Breadcrumbs = React.createClass({
	getInitialState: function () {
		return {
			categories: [],
			products: [],
			product: {},
			links: []
		};
	},
	componentWillMount: function () {		
		PurchasesStore.bind('change', this.changeCollection);
		PurchasesStore.bind('categoryReceived', this.categoryReceived);
		PurchasesStore.bind('get-product', this.productReceived);
	},
	componentWillUnmount: function () {
		PurchasesStore.unbind('change', this.changeCollection);		
		PurchasesStore.unbind('categoryReceived', this.categoryReceived);
		PurchasesStore.unbind('get-product', this.productReceived);
	},
	changeCollection: function () {
		// console.log('breadcrumbs collection:', PurchasesStore.collection);
		PurchasesActions.getCategoriesTree();
		this.setState({
			collection: PurchasesStore.collection
		});				
	},
	productReceived: function () {
		// console.log('breadcrumbs product:', PurchasesStore.product);
		PurchasesActions.getCategoriesTree();
		this.setState({
			product: PurchasesStore.product
		});			
	},
	categoryReceived: function () {
		// console.log('breadcrumbs categories:', PurchasesStore.categories);
		this.setState({
			categories: PurchasesStore.categories
		});		

		// только когда получены категории и коллекция разруливаем breadcrumbs
		// получение url
        var url = $(location).attr('pathname');
        var parse_url = url.split('/')[1];

        // Проверяем где находимся на момент загрузки страницы
        // проверка что это категория
        var is_category = parse_url.slice(0,8) == 'category';
        // console.log('is_category: ', is_category);
        // проверка что это закупка
        var is_purchase = url.split('/')[1] == 'purchases';
        // console.log('is_purchase: ', is_purchase);
        // проверка что это продукт
        var is_product = url.split('/')[1] == 'products';
        // console.log('is_product: ', is_product);
        
		if (url == '/') {
        	this.setState({
        		links: [
        			{
        				'name': 'Главная',
        				'href': '/'
        			}
        		]
        	});
        } else if (is_category) {
        	var current_category_slug = parse_url.slice(9);
        	var cat_tree = getCatTree(this.state.categories, current_category_slug);

        	this.setState({
        		links: cat_tree
        	});
        } else if (is_purchase){        	
			this.setState({
        		links: [
        			{
        				'name': 'Главная',
        				'href': '/'
        			},
        			{
        				'name': this.state.collection[0].name,
        				'href': '/purchases/' + this.state.collection[0].id + '/'
        			}
        		]
        	});
        } else if (is_product) {        	
        	var product_tree = getProdTree(this.state.categories, this.state.product);
        	this.setState({
        		links: product_tree
        	});
        };
	},
	render: function () {
		var links = this.state.links;
		var list = links.map(function (link, count) {			
			if (count == links.length - 1) {				
				return (
					<li className="active">{link.name}</li>
				);
			} else {
				return (
					<li><a href={link.href}>{link.name}</a></li>
				);
			}
		});
		return (
			<div className="container">
                <ul className="breadcrumb">
                	{list}                    
                </ul>
            </div>   
		);
	}
});


module.exports = Breadcrumbs;