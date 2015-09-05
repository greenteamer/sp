var _ = require('underscore');

var Methods = {
	convertCategoriesToFlatProducts: function (collection) {
		console.log('Methods convertCategoriesToFlatProducts collection:', collection);
		tmp_collection = [];
        collection.forEach(function (category){
            var collection = category.category_purchase;            
            category.category_purchase.forEach(function (purchase) {
                purchase.catalogs.forEach(function (catalog) {
                    catalog.product_catalog.forEach(function (product) {
                        product.cpp_catalog = catalog.cpp_catalog;
                        tmp_collection.push(product);
                    });
                });
            });
        });  
        console.log('Methods convertCategoriesToFlatProducts collection result:', tmp_collection);
        return tmp_collection;	
	},
	convertPurchasesToFlatProducts: function (collection) {
		console.log('Methods convertPurchasesToFlatProducts collection:', collection);
		tmp_collection = [];
        
            collection.forEach(function (purchase) {
                purchase.catalogs.forEach(function (catalog) {
                    catalog.product_catalog.forEach(function (product) {
                        product.cpp_catalog = catalog.cpp_catalog;
                        tmp_collection.push(product);
                    });
                });
            });       
        console.log('Methods convertPurchasesToFlatProducts collection result:', tmp_collection);
        return tmp_collection;	
	}
}


module.exports = Methods;