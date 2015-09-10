// -- * -- CHACKPROPERTIES -- * --
// chackProperties - проверка существования комбинации свойств в товаре
// принимает 2 обязательных параметра:
// cpp_properties - массив свойств, который находится в состоянии компонента формы (включает в себя обязательный параметр value - который лежит в объекте каждого свойства, которое заполняет пользователь)
// product_properties - строка в которой через ";" перечислены все возможные комбинации свойств данного товара
// функция chackProperties проверяет все ли параметры заполнил пользователь, создает из их значений строку в которой они перечислены через "," и проверяет эту строку на совпадение среди всех возможных вариантов
// -- * --

var _ = require('underscore');
var $ = require('jquery');
var snackbar = require('../../../lib/snackbar.js');

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
	},
    chackProperties: function(cpp_properties, product_properties){        
        // РЕАЛИЗАЦИЯ ПРОВЕРКИ СУЩЕСТВОВАНИЯ КОМБИНАЦИИ СВОЙСТВ        
        var properties_filled = _.every(cpp_properties,function (property) {
            // проверяем все ли свойства заполнены
            // _.every - возвращает true если все итерации функции вернули true
            return property.value != undefined;
        });        
        if (properties_filled) {
            var values_str = _.pluck(cpp_properties, 'value').join(',');
            // _.pluck - возвращает массив состоящий из значений полей 'value' объектов массива
            // join - создает из массива выбранных параметров строку параметров через ','
            if (_.contains(product_properties.split(';'), values_str)) {
                // _.contains - возвращает true если массив содежит элемент values_str
                $.snackbar({timeout: 5000, content: 'Товары с данными характеристиками найдены' });
                return true;
            } else {   
                // выводим сообщение и возвращяем false             
                $.snackbar({timeout: 5000, content: 'Нет товара с такими характеристиками, пожалуйста, попробуйте другие варианты' });
                return false;
            }
        };
    },
}


module.exports = Methods;