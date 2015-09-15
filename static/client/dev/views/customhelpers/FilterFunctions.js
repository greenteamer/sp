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
	filterByCategory: function (purchases, products_collection) {
		var flat_category_products = Methods.convertPurchasesToFlatProducts(purchases);		

		var result_collection = _.filter(products_collection, function (product) {
			return _.some(flat_category_products, function function_name (cat_product) {
				return product.id == cat_product.id;
			});
		});

		return result_collection;
	},	
	filterFlow: function (filter, collection, categories){
		
		console.log('filterFlow PurchasesStore filter: ', filter.filter_state);
		console.log('filterFlow PurchasesStore collection: ', collection);
		console.log('filterFlow PurchasesStore categories: ', categories);	

		var result_by_cat = [];
		var result_by_price = [];
		var sorted_collection = [];

	 	if (collection.length > 0 && categories.length > 0) {
			// конвертируем изначальную коллекцию в простую (массив товаров)
			var initial_collection = Methods.convertCategoriesToFlatProducts(collection);
			console.log('filterFlow PurchasesStore initial_collection: ', initial_collection);	
			
			if (filter.filter_state.category != undefined){
				// фильтруем начальную коллекцию по категории
				var cat_purchases = Methods.getPurchasesFromCategories(categories, filter.filter_state.category);
				console.log('filterFlow by cat cat_purchases: ', cat_purchases);	
				result_by_cat = this.filterByCategory(cat_purchases, initial_collection);
			};	
			if(filter.filter_state.price != undefined){			
				// фильтруем начальную коллекцию по цене
				var result_by_price = this.filterByPrice(initial_collection, filter.filter_state.price);
			};
			
			// объединяем результат
			console.log('filterFlow result_by_price: ', result_by_price);
			console.log('filterFlow result_by_cat: ', result_by_cat);
			var result = Methods.unionProductCollections(result_by_price, result_by_cat);
			console.log('filterFlow PurchasesStore result: ', result);	

			sorted_collection = _.sortBy(result, function(product){ 
	        	return product.price; 
	        });
        };

		return sorted_collection;			
	}
};


module.exports = Functions;