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
		tmp_collection = [];                             
        collection.forEach(function (purchase) {
            purchase.catalogs.forEach(function (catalog) {
                catalog.product_catalog.forEach(function (product) {
                    product.cpp_catalog = catalog.cpp_catalog;
                    tmp_collection.push(product);
                });
            });
        });        
        return tmp_collection;	
	},
    getAllNestedCategories: function (data, category_slug) {
        // ПОДГОТОВКА КОЛЛЕКЦИИ ВСЕХ ВЛОЖЕННЫХ КАТЕГОРИЙ
        // *** 
        // ВАЖНО: работает только с вложенностью не более 3 уровней 
        // ***
        // data - коллекция всех категорий категорий
        // category_slug - слаг категории относительно которой мы работаем
        var all_categories = [];
        if (category_slug != undefined && category_slug != '') {
            var category = _.find(data, function (category) {
                // находим категорию на которую перешел пользователь
                return category.slug == category_slug;
            });    

            all_categories = _.filter(data, function (cat) {
                // Фильтруем все дочерние категории основной
                return cat.parent == category.id;
            });

            var all_categories_deep = _.map(all_categories, function (first_level_cat) {
                // проходимся по всем дочерним категориям
                // каждую итерацию фильтруем все категории по parent признаку
                // получаем всех предков изначальной категории
                return _.filter(data, function (cat) {
                    return cat.parent == first_level_cat.id;
                });                          
            });

            // приводим массив к элементарному виду что бы избежать [ [a], [[b]]]
            all_categories_deep = _.flatten(all_categories_deep, true);

            //объединяем полученные результаты по подкатегориям и по подподкатегориям
            all_categories = _.union(all_categories, all_categories_deep);        
        }else {
            // если slug = undefined или '' то возвращаем весь массив
            all_categories = data;
        }
        // console.log('Methods getAllNestedCategories all_categories: ', all_categories);
        return all_categories;
    },
    getPurchasesFromCategories: function (data, category_slug) {
        // ПОДГОТОВКА КОЛЛЕКЦИИ ЗАКУПОК КАТЕГОРИИ
        // data - строковая переменная "slug" категории
        // console.log('Methods getPurchasesFromCategories data, category_slug: ', data, category_slug);
        var category = _.find(data, function (category) {
            // находим категорию на которую перешел пользователь
            return category.slug == category_slug;
        });
        // console.log('Methods getPurchasesFromCategories find category by slug: ', category);  
        // получаем все вложенные категории
        var all_categories = this.getAllNestedCategories(data, category_slug);        
        // добавляем в массив родительскую категорию
        all_categories.unshift(category);
        // console.log('Methods getPurchasesFromCategories  getAllNestedCategories: ', all_categories);

        // создаем массив из всех значений поля "category_purchase"
        var all_purchases_arr = _.pluck(all_categories, "category_purchase");
        // console.log('Methods getPurchasesFromCategories  get all purchases from all categories: ', all_purchases_arr);
        // приводи к элементарному виду
        var all_purchases = _.flatten(all_purchases_arr, true);
        // console.log('Methods getPurchasesFromCategories all_purchases: ', all_purchases);
        return all_purchases;
    },    
    getCatalogsFromCategories: function (initial_categories, category_slug) {
        // console.log('Methods.getCatalogsFromCategories all_categories: ', all_categories);
        var category = _.find(initial_categories, function (category) {
            // находим категорию на которую перешел пользователь
            return category.slug == category_slug;
        });
        // console.log('Methods getPurchasesFromCategories find category by slug: ', category);  
        // получаем все вложенные категории
        var all_categories = this.getAllNestedCategories(initial_categories, category_slug);        
        // добавляем в массив родительскую категорию
        all_categories.unshift(category);

        // получаем id всех категорий включая вложенные
        var category_id_arr = _.pluck(all_categories, 'id');
        // console.log('Methods getPurchasesFromCategories  category_id_arr: ', category_id_arr);

        // ПОЛУЧАЕМ ВСЕ КАТАЛОГИ
        // создаем массив из всех значений поля "category_purchase"
        var all_purchases_arr = _.pluck(initial_categories, "category_purchase");
        // console.log('Methods getPurchasesFromCategories  get all purchases from all categories: ', all_purchases_arr);
        // приводим к элементарному виду
        var all_purchases = _.flatten(all_purchases_arr, true);
        // console.log('Methods getPurchasesFromCategories all_purchases: ', all_purchases);
        var all_catalogs_arr = _.pluck(all_purchases, "catalogs");
        // приводи к элементарному виду
        var all_catalogs = _.flatten(all_catalogs_arr, true);

        // ФИЛЬТРУЕМ СОГЛАСНО category_id_arr
        var result = _.map(category_id_arr, function (id) {
            // генерируем массив каталогов
            return _.filter(all_catalogs, function (catalog) {
                // получаем каталог если хоть один id его категрии совпадает
                return _.some(catalog.categories, function (category_id) {                    
                    return category_id === id; 
                });
            });
        });
        result = this.unique(_.flatten(result, true));
        // console.log('Methods getCatalogsFromCategories result: ', result);
        return result;
    },
    convertCatalogsToFlatProducts: function (catalogs) {
        // console.log('Methods convertCatalogsToFlatProducts catalogs: ', catalogs);
        // делаем из массива каталогов массив продуктов
        var new_products_arr = _.pluck(catalogs, 'product_catalog');
        new_products_arr = _.flatten(new_products_arr, true);
        return new_products_arr;
    },
	convertPurchasesToFlatProducts: function (collection) {
		tmp_collection = [];
        // console.log('Methods convertPurchasesToFlatProducts collection: ', collection);
        if (collection.length > 0) {
            collection.forEach(function (purchase) {
                purchase.catalogs.forEach(function (catalog) {
                    catalog.product_catalog.forEach(function (product) {
                        product.cpp_catalog = catalog.cpp_catalog;                        
                        tmp_collection.push(product);
                    });
                });
            });       
        };
        return tmp_collection;	
	},
    unique: function (arr) {
        // ВОЗВРАЩАЕТ МАССИВ УНИКАЛЬНЫХ ЭЛЛЕМЕНТОВ массива arr
        // обязательное условие: у объектов массива должен быть атрибут id
        // console.log('Methods.unique start , arr: ', arr);
        var arr_id = _.uniq(_.pluck(arr, 'id'));  // вернет массив уникальных id -шников массива arr
        // console.log('Methods.unique unoque id arr: ', arr_id);
        var result = _.map(arr_id, function (id) {
                // возвращаем первый эллемент массива arr, 
                // id которого есть в массиве уникальных id -шников
                return _.find(arr, function (el) {
                    return el.id === id;
                });
            });
        // console.log('Methods.unique unoque result: ', result);
        return result;
    },
    unionProductCollections: function (collection1, collection2) {
        // функция объединения 2 коллекций продуктов
        // если первая коллекция пуста - пишем в консоле лог
        // console.log('Method.unionProductCollections COLLECTION1: ', 'length: ', collection1.length, collection1);
        // console.log('Method.unionProductCollections COLLECTION2: ', 'length: ', collection2.length, collection2);
        
        // if (collection1.length > 0 && collection2.length > 0) {

        var c1 = _.pluck(collection1, 'id');  // создаем массив id -шников 1 коллекции  
        var c2 = _.pluck(collection2, 'id');  // создаем массив id -шников 2 коллекции
        var index_arr = _.intersection(c1, c2);  // объединяем уникальные id -шники в один массив
        var union = _.union(collection1, collection2);  // объединяем оба массива с прдуктами 
        var result = _.map(index_arr, function (id) {
            // возвращаем первый эллемент массива union, 
            // id которого есть в массиве уникальных id -шников
            return _.find(union, function (prod) {
                return prod.id === id;
            });
        });

        // console.log('test index_arr: ', 'length: ', index_arr.length, index_arr);
        // console.log('test result: ', 'length: ', result.length, result);      

        return result;
    },
    chackProperties: function(cpp_properties, product_properties){        
        // РЕАЛИЗАЦИЯ ПРОВЕРКИ СУЩЕСТВОВАНИЯ КОМБИНАЦИИ СВОЙСТВ        
        var properties_filled = _.every(cpp_properties,function (property) {
            // проверяем все ли свойства заполнены
            // _.every - возвращает true если все итерации функции вернули true
            return property.value !== undefined;
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
        }
    },
    getCategorySlug: function() {
        // получение slug категории по текущему url
        var url = $(location).attr('pathname');
        var parse_url = url.split('/')[1];        
        var current_category_slug = parse_url.slice(9);

        // console.log('get url', url);
        if (url.split('/')[1] == 'purchases') {
            // console.log('its purchase url');
            current_category_slug = 'purchase';
        };

        return current_category_slug;    
    },
    getPurchaseIdByUrl: function () {
        // получение категорий к которым привязаны каталоги закупки
        var url = $(location).attr('pathname');
        var purchase_id = url.split('/')[2];
        return purchase_id;
    }
};


module.exports = Methods;