var $ = require('jquery');
var _ = require('underscore');

var Methods = require('./Methods.js');
var PurchasesActions = require('../../actions/PurchasesActions.js');


var Functions = {
	filterByPrice: function (products_collection, values) {
		var tmp_filtered_сollection = _.filter(products_collection, function (product) {
            return product.price >= values[0] && product.price <= values[1] ;
        });

        return tmp_filtered_сollection;
	},
	filterByCategory: function (flat_products, products_collection) {
		// var flat_products = Methods.convertPurchasesToFlatProducts(purchases);		
		// console.log('Filter.filterByCategory flat_products: ', flat_products);
		// console.log('Filter.filterByCategory products_collection: ', products_collection);
		var result_collection = _.filter(products_collection, function (product) {
			return _.some(flat_products, function function_name (cat_product) {
				return product.id == cat_product.id;
			});
		});

		return result_collection;
	},	
	filterFlow: function (filter, initial_collection, categories){
		// ФУНКЦИЯ ФИЛЬТРАЦИИ ТОВАРОВ
		// функция принимает 3 параметра:
		// filter - текущие состояние фильтра из Store.filter
		// initial_collection - изначальная коллекция преобразованная в Dispatcher.register во flat коллекцию продуктов
		// categories  - коллекция всех категорий из Store.categories

		// ПРОВЕРКА ВХОДЯЩИХ ДАННЫХ
		console.log('start filter flow');
		console.log('filterFlow PurchasesStore filter: ', filter.filter_state);
		console.log('filterFlow PurchasesStore initial_collection: ', initial_collection);
		console.log('filterFlow PurchasesStore categories: ', categories);	
		var result_by_cat = [];
		var result_by_price = [];
		if (filter.filter_state.category != undefined && filter.filter_state.category != ''){
			console.log('Filter.filterFlow start category filter');
			var cat_catalogs = Methods.getCatalogsFromCategories(categories, filter.filter_state.category);
			console.log('Filter.filterFlow Methods.getCatalogsFromCategories cat_catalogs:', cat_catalogs);

			var flat_category_products = Methods.convertCatalogsToFlatProducts(cat_catalogs);	
			console.log('Filter.filterFlow flat_category_products:', flat_category_products);
			result_by_cat = flat_category_products;
		} else if (filter.filter_state.category == ''){
			// если приходит пустой фильтр с категорией - возвращаем все изначальные товары
			var result_by_cat = initial_collection;
		}

		if(filter.filter_state.price != undefined){			
			// фильтруем начальную коллекцию по цене				
			result_by_price = this.filterByPrice(initial_collection, filter.filter_state.price);
			console.log('Filter.filterFlow by category result_by_price: ', 'length: ', result_by_price.length, result_by_price);
		};
		
		// объединяем результат			
		var result = Methods.unionProductCollections(result_by_price, result_by_cat);
		console.log('Filter.filterFlow filter result: ', result);	

		var sorted_collection = _.sortBy(result, function(product){ 
        	return product.price; 
        });
        console.log('Filter.filterFlow sorted_collection result: ','length: ', sorted_collection.length, sorted_collection);	        

		return sorted_collection;			
	}
};


module.exports = Functions;