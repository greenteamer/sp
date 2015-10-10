var $ = require('jquery');
var _ = require('underscore');

var Methods = require('./Methods.js');
var PurchasesActions = require('../../actions/PurchasesActions.js');


var Functions = {

	search_by_id: function  (purchase_id, catalog_id, product_id, allPurchases ) {
    console.log('search_by_id functions purchase_id: ', purchase_id);
    console.log('search_by_id functions catalog_id: ', catalog_id);
    console.log('search_by_id functions product_id: ', product_id);


    // var tmp_purch = _.filter(allPurchases, function (purch) {
    //   return purchase_id.indexOf(purch.id) != -1 ;
    // });
    // var new_purch = _.map(tmp_purch, function (purch) {
    //   purch.catalogs = _.map(
    //     _.filter(purch.catalogs, function (cat) {
    //       // фильтруем массив каталогов этой закупки и 
    //       // оставляем в очередной закупке только наши каталоги                        
    //       return catalog_id.indexOf(cat.id) != -1 ;
    //       // затем проходим по каждой фильтруя продукты
    //     }), function (cat) {
    //       // ЧИТАТЬ ОТСЮДА
    //       cat.product_catalog = _.filter(cat.product_catalog, function (prod) {
    //         // меняем очередной каталог так что в нем остаются только наши продукты
    //         return product_id.indexOf(prod.id) != -1;
    //       });
    //       return cat;
    //     });
    //   return purch;                
    // });
    // return new_purch;
    var new_purch = _.map(allPurchases, function (purch) {
      purch.catalogs = _.map(purch.catalogs, function (cat) {
          // ЧИТАТЬ ОТСЮДА
          cat.product_catalog = _.filter(cat.product_catalog, function (prod) {
            // меняем очередной каталог так что в нем остаются только наши продукты
            return product_id.indexOf(prod.id) != -1;
          });
          return cat;
        });
      return purch;                
    });

    var purch_list = [];
    _.each(new_purch, function (purch) {
    	var catal_list = [];

    	_.each(purch.catalogs, function (cat) {
    		if (cat.product_catalog.length > 0) {
    			catal_list.push(cat);
    		};
    	});

    	if (catal_list.length > 0) {
    		purch.catalogs = catal_list;
    		purch_list.push(purch);
    	};
    });

    return purch_list;
	},


	search: function (allPurchases, allCategories, allCatalogs, search_obj) {
		console.log('search functions allPurchases: ', allPurchases);
		console.log('search functions allCategories: ', allCategories);
		console.log('search functions search_obj: ', search_obj);
		var query = search_obj.search_state.query;
		query = $.trim(query);

		// создаем массивы id шников что бы потом по ним сравнивать
		var purch_arr = _.filter(allPurchases, function (purch) {
			// возвращяем массив закупок если есть совпадения в названии закупки
      return purch.name.toLowerCase().search(query) != -1;
    });
    var purch_id_arr = _.pluck(purch_arr, 'id');
		// получаем массив айдишников категорий
		// console.log('search functions purch_id_arr: ', purch_id_arr);
		var catigories_arr = _.filter(allCategories, function (category) {
				return category.name.toLowerCase().search(query) != -1;
			});
		var categories_id_arr = _.pluck(catigories_arr, 'id');
		// console.log('search functions categories_id_arr: ', categories_id_arr);
		// получаем массив айдишников каталогов
		var catalogs_arr = _.filter(allCatalogs, function (catalog) {
				return catalog.catalog_name.toLowerCase().search(query) != -1;
			});
		var catalogs_id_arr = _.pluck(catalogs_arr, 'id');
		// console.log('search functions catalogs_id_arr: ', catalogs_id_arr);
		// получаем массив айдишников продуктов 
		// получаем массив массивов продуктов и приводим его к простейшему виду
		var all_products_arr = _.flatten(_.pluck(allCatalogs, 'product_catalog'), true);
		var products_arr = _.filter(all_products_arr, function (prod) {
			return prod.product_name.toLowerCase().search(query) != -1;
		});
		var products_id_arr = _.pluck(products_arr, 'id');
		// console.log('search functions products_arr: ', products_id_arr);


    console.log('search functions purch_id: ', purch_id_arr);
    console.log('search functions catal_id: ', categories_id_arr);
    console.log('search functions prod_id: ', products_id_arr);
		var result = this.search_by_id(purch_id_arr, categories_id_arr, products_id_arr, allPurchases);
		console.log('search functions result: ', result);

		return result;
		// var filter_by_purch = _.filter(allPurchases, function (purch) {
		// 	// возвращяем массив закупок если есть совпадения в названии закупки
  //     return purch.name.toLowerCase().search(query) != -1;
  //   });

  //   var filter_by_categories = _.filter(allPurchases, function (purch) {
		// 	// возвращяем массив закупок если есть совпадения в названии категории			
  //     return _.some(purch.categories, function (category_id) {
  //     	return catigories_id_arr.indexOf(category_id) != -1;
  //     });
  //   });

  //   var filter_by_catalogs = _.filter(allPurchases, function (purch) {
		// 	// возвращяем массив закупок если есть совпадения в названии каталога
		// 	return _.some(purch.catalogs, function (catalog) {
		// 		console.log('search functions filter_by_catalogs catalog_id: ', catalog);				
  //     	return catalogs_id_arr.indexOf(catalog.id) != -1;
  //     });
  //   });

  //   console.log('search functions filter_purch: ', filter_by_purch);
  //   console.log('search functions filter_categories: ', filter_by_categories);
		// console.log('search functions filter_by_catalogs: ', filter_by_catalogs);
	}
};


module.exports = Functions;






















