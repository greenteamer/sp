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
		console.log('Filter.filterByCategory flat_products: ', flat_products);
		console.log('Filter.filterByCategory products_collection: ', products_collection);
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
		// console.log('start filter flow');
		// console.log('filterFlow PurchasesStore filter: ', filter.filter_state);
		// console.log('filterFlow PurchasesStore initial_collection: ', initial_collection);
		console.log('filterFlow PurchasesStore categories: ', categories);	

		var result_by_cat = [];
		var result_by_price = [];
		var sorted_collection = [];

	 	// if (collection.length > 0 && categories.length > 0) {
			// конвертируем изначальную коллекцию в простую (массив товаров)
			// var initial_collection = Methods.convertCategoriesToFlatProducts(collection);
			// console.log('filterFlow PurchasesStore initial_collection: ', initial_collection);	
			
			if (filter.filter_state.category != undefined){
				// фильтруем начальную коллекцию по категории
				var cat_purchases = Methods.getPurchasesFromCategories(categories, filter.filter_state.category);
				// console.log('Filter.filterFlow Methods.getPurchasesFromCategories result: ', 'length: ', cat_purchases.length, cat_purchases);		
				// result_by_cat = this.filterByCategory(cat_purchases, initial_collection);
				var flat_category_products = Methods.convertPurchasesToFlatProducts(cat_purchases);	
				// result_by_cat = this.filterByCategory(flat_category_products, initial_collection);
				result_by_cat = flat_category_products;
				console.log('Filter.filterFlow by category result_by_cat: ', 'length: ', result_by_cat.length, result_by_cat);
			};	

			if(filter.filter_state.price != undefined){			
				// фильтруем начальную коллекцию по цене				
				var result_by_price = this.filterByPrice(initial_collection, filter.filter_state.price);
				console.log('Filter.filterFlow by category result_by_price: ', 'length: ', result_by_price.length, result_by_price);
			};
			
			// объединяем результат			
			var result = Methods.unionProductCollections(result_by_price, result_by_cat);
			console.log('Filter.filterFlow filter result: ', result);	

			sorted_collection = _.sortBy(result, function(product){ 
	        	return product.price; 
	        });
	        console.log('Filter.filterFlow sorted_collection result: ','length: ', sorted_collection.length, sorted_collection);	
        // };

		return sorted_collection;			
	}
};


module.exports = Functions;