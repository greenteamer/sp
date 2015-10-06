var PurchasesDispatcher = require('../dispatcher/PurchasesDispatcher.js');
var PurchasesActions = require('../actions/PurchasesActions.js');
var MicroEvent = require('microevent');
var merge = require('merge');
var $ = require('jquery');
var _ = require('underscore');
var Cookies = require('js-cookie');
var snackbar = require('../../lib/snackbar.js');

var Methods = require('../views/customhelpers/Methods.coffee');
var FilterFunctions = require('../views/customhelpers/FilterFunctions.js');


function get_search_result_purchases(query){
    console.log('start get_search_result_purchases function');
    console.log('get_search_result_purchases function query:', query);
    result = [];
    PurchasesStore.search_result_collection = result;
    PurchasesStore.query_text = query;
    PurchasesStore.searchResult();
    return result;
}


var PurchasesStore = merge(MicroEvent.prototype, {
    
    // состояние отображений
    view_state: {
        view_type: '',
        view_width: 12,
        view_by: '',
        view_page: ''
    },
    changeViewState: function(){
        this.trigger('changeViewState');
    },

    // состояние фильтра приложения
    filter: {
        filter_state: {
            price: [],
            category: ''
        },
        filtered_collection: []
    },
    filterTrigger : function () {
        this.trigger('filterTrigger');    
    },

    user: {},
    organizer_profiles: [],
    organizerCollectionChange: function () {
        this.trigger('organizersTrigger');  
    },

    // начальная коллекция всех закупок
    initial_purchases: [],
    getInitialPurchases: function () {
        this.trigger('getInitialPurchases');  
    },

    // collection - массив закупок
    collection: [], 
    cartitems: [],
    
    categories: [],
    categoryReceived: function () {
        this.trigger('categoryReceived');  
    },

    catalogs: [],
    catalogsReceived: function () {
        this.trigger('catalogsReceived');  
    },

    search_result_collection: [],
    query_text: '',
    searchResult: function () {
        console.log('Store searchResult start');
        this.trigger('searchResult');  
    },

    product_fast_view: {},
    purchase_id_fast_view: 0,
    
    product: {},
    getProduct: function(){
        this.trigger('get-product');
    },

    benefits: [],
    modal_photo: {},
    photoView: function(){
        this.trigger('photoView');
    },

    message_modal: {},
    messageView: function () {
        console.log('PurchasesStore messageView trigger message_modal: ', this.message_modal);
        this.trigger('messageView');
    },

    // for purchase page
    purchase: [],
    chengePurchaseDetail: function  () {
        this.trigger('chengePurchaseDetail');
    },
    
    collectionChange: function(){
        this.trigger('change');
    },
    modalView: function(){
        this.trigger('modal');
    },    
    changeBenefits: function(){
        this.trigger('changeBenefits');
    }    
});


PurchasesDispatcher.register(function (payload) {
    switch (payload.actionType) {

        // изменение отображения компонентов
        case 'change-view-type':
            PurchasesStore.view_state.view_type = payload.type;
            PurchasesStore.changeViewState();
            break;

        case 'set-view-width':
            PurchasesStore.view_state.view_width = payload.num;
            PurchasesStore.changeViewState();
            break;
        //конец изменения отображения компонентов

        case 'get-popular-promo':
            $.ajax({
                url: '/api/v1/popular-promos/',
                dataType: 'json',
                cache: false,
                success: (function (data) {
                    PurchasesStore.collection = data;
                    PurchasesStore.collectionChange();

                }).bind(this),
                error: (function (xhr, status, err) {
                    console.log('error fetchin collection');
                }).bind(this)
            });            
            break;

        case 'get-new-promo':
            $.ajax({
                url: '/api/v1/new-promos/',
                dataType: 'json',
                cache: false,
                success: (function (data) {
                    PurchasesStore.collection = data;
                    PurchasesStore.collectionChange();

                }).bind(this),
                error: (function (xhr, status, err) {
                    console.log('error fetchin collection');
                }).bind(this)
            });
            break;

        case 'get-hot-purchases':
            $.ajax({
                url: '/api/v1/hot-purchases/',
                dataType: 'json',
                cache: false,
                success: (function (data) {
                    PurchasesStore.collection[0].promo_purchase = data;
                    PurchasesStore.collection[0].name = "Горящие закупки";
                    PurchasesStore.collectionChange();

                }).bind(this),
                error: (function (xhr, status, err) {
                    console.log('error fetchin collection');
                }).bind(this)
            });
            break;

        case 'get-search-results':
            var result = get_search_result_purchases(payload.query);
            console.log('Store get_search_result_purchases: ');
            //$.ajax({
            //    url: '/api/v1/search/purchases/' + '?query=' + payload.query,
            //    dataType: 'json',
            //    cache: false,
            //    success: (function (data) {
            //        PurchasesStore.search_result_collection = data;
            //        console.log('Store search result data: ', data);
            //        PurchasesStore.query_text = payload.query;
            //        PurchasesStore.collectionChange();
            //    }).bind(this),
            //    error: (function (xhr, status, err) {
            //        console.log('error fetchin collection');
            //    }).bind(this)
            //});
            break;

        case 'add-to-cart':
            var csrftoken = Cookies.get('csrftoken');
            var tmp_properties = '';
            payload.item.cpp_properties.forEach(function (property, index){
                if (index != 0) {
                    tmp_properties = tmp_properties + ',' + payload.item.cpp_properties[index].value;
                } else {
                    tmp_properties = payload.item.cpp_properties[index].value;
                }
            });
            $.post(
                "/add-to-cart/",
                {
                    ajax: 'add_to_cart',
                    csrfmiddlewaretoken: csrftoken,
                    product: payload.item.product.id,
                    product_properties: tmp_properties,
                    quantity: payload.item.product.count
                }
            ).success(
                function (data) {
                    var message = "товар успешно добавлен в корзину";
                    $.snackbar({timeout: 5000, content: message });
                    PurchasesActions.getCartItems();
                })
            .error(
                function (data) {
                    var message = "Товара с такими свойствами нет, попробуйте другие варианты";
                    $.snackbar({timeout: 5000, content: message });
                    console.log("Ошибка post запроса");
                });
            break;

        case "get-categories":
            $.get("/api/v1/categories/")
                .success(function (data) {
                    // console.log("Store get categories success data: ", data);
                    PurchasesStore.categories = data;
                    PurchasesStore.categoryReceived();
                })
                .error(function () {
                    console.log("get-categories Ошибка get запроса"); 
                });
            break;

        case "get-catalogs":
            $.get("/api/v1/catalogs/")
                .success(function (data) {
                    // console.log("Store get categories success data: ", data);
                    PurchasesStore.catalogs = data;
                    PurchasesStore.catalogsReceived();
                })
                .error(function () {
                    console.log("get-categories Ошибка get запроса"); 
                });
            break;

        case "get-category-purchases":
            $.ajax({
                url: '/api/v1/categories/',
                dataType: 'json',
                cache: false,
                success: (function(data){                    
                    // getPurchasesFromCategories - подробное описание в файле customhelpers/Methods.js
                    PurchasesStore.collection = Methods.getPurchasesFromCategories(data, payload.category);
                    PurchasesStore.collectionChange();    
                }).bind(this),
                error: (function (xhr, status, err) {
                        console.log('error fetchin collection');
                    }).bind(this)
            });
            break;

        case "get-cart-items":
            $.ajax({
                url: '/api/v2/cart-items/',
                dataType: 'json',
                cache: false,
                success: (function(data){
                    PurchasesStore.cartitems = data;
                    PurchasesStore.collectionChange();
                }).bind(this),
                error: (function (xhr, status, err) {
                        console.log('error fetchin collection');
                    }).bind(this)
                });
            break;

        case "get-organizers":
            $.ajax({
                url: '/api/v1/organizers/',
                dataType: 'json',
                cache: false,
                success: (function(data){
                    // console.log('Store get-organizers data: ', data);
                    PurchasesStore.organizer_profiles = data;
                    PurchasesStore.organizerCollectionChange();
                }).bind(this),
                error: (function (xhr, status, err) {
                        console.log('error fetch organizers collection');
                    }).bind(this)
                });
            break;

        case "fast-show-product":
            console.log('PurchasesStore start fast-show-product');
            //передаем продукт которй быстро хочет посмотреть человек
            PurchasesStore.product_fast_view = payload.product;
            PurchasesStore.product_fast_view.cpp_catalog = payload.cpp_catalog;
            PurchasesStore.purchase_id_fast_view = payload.purchase_id;
            PurchasesStore.modalView();
            break;

        case "show-photo":
            PurchasesStore.modal_photo = payload.photo;
            PurchasesStore.photoView();
            break;

        case "show-message-modal":
            console.log('PurchasesStore start show-message-modal');
            PurchasesStore.message_modal = payload.message;
            PurchasesStore.messageView();            
            break;

        case "get-product":
            //получаем продукт по id
            var url = '/api/v1/products/' + payload.product_id + "/";
            $.ajax({
                //получаем товар
                url: url,
                dataType: "json",
                cache: false,
                success: (function(data){
                    var url_catalog = '/api/v1/catalogs/' + data.catalog + "/";
                    var tmp_product = data;
                    $.ajax({
                        //получаем свойства каталога и добавляем в товар
                        url: url_catalog,
                        dataType: "json",
                        cache: false,
                        success: (function(data){
                            tmp_product.cpp_catalog = data.cpp_catalog;
                            tmp_product.catalog_obj = data;
                            PurchasesStore.product = tmp_product;
                            PurchasesStore.getProduct();
                        }).bind(this),
                        error: (function(){
                            console.log('ups, something went wrong');
                        }).bind(this)
                    });
                }).bind(this),
                error: (function(xhr, status, err){
                    console.log('error fetchin collection');
                }).bind(this)
            });
            break;

        case "get-benefits":
            $.ajax({
                url: "/api/v1/benefits/",
                dataType: "json",
                cache: false,
                success: function(data){
                    PurchasesStore.benefits = data;
                    PurchasesStore.changeBenefits();
                },
                error: function(){
                    console.log('oups, something went wrong');
                }
            });
            break;

        case "get-initial-purchases":
            console.log('Store get-initial-purchases start');
            $.ajax({
                url: "/api/v1/purchases/",
                dataType: 'json',
                cache: false,
                success: function (data) {
                    PurchasesStore.initial_purchases = data;
                    PurchasesStore.getInitialPurchases();
                },
                error: function () {
                    console.log('error ajax initial purchases fetch');
                }
            });
            break;

        case 'get-current-purchase-datail':
            var url = '/api/v1/purchases/' + payload.id + '/';
            $.ajax({
                url: url,
                dataType: 'json',
                cache: false,
                success: (function(data){                    
                    // PurchasesStore.purchase = [];
                    // PurchasesStore.purchase.push(data);
                    // PurchasesStore.chengePurchaseDetail();                    
                    PurchasesStore.collection.push(data);
                    PurchasesStore.collectionChange();
                }).bind(this),
                error: (function(){
                    console.log('sory, something went wrong');
                }).bind(this),
            });
            break;  

        case 'filter-collection':
            PurchasesStore.filter.filtered_collection = payload.filtered_collection;
            PurchasesStore.filterTrigger();
            break;

        case 'filter-by-category':
            PurchasesStore.filter.filter_state.category = payload.category_slug;
            // filterFlow - основной поток фильтра в который приходят исходные данные и который разруливает все остальное
            if (PurchasesStore.collection.length > 0 && PurchasesStore.categories.length > 0) {
                // конвертируем изначальную коллекцию в простую (массив товаров)
                // console.log('filter-by-category PurchasesStore.collection', PurchasesStore.collection);
                var initial_collection = Methods.convertPurchasesToFlatProducts(PurchasesStore.collection);

                var result = FilterFunctions.filterFlow(PurchasesStore.filter, initial_collection, PurchasesStore.categories);

                PurchasesStore.filter.filtered_collection = result;
                PurchasesStore.filterTrigger();
            };
            break;

        case 'filter-by-price':
            PurchasesStore.filter.filter_state.price = payload.price;            
            // filterFlow - основной поток фильтра в который приходят исходные данные и который разруливает все остальное
            if (PurchasesStore.collection.length > 0 && PurchasesStore.categories.length > 0) {
                // конвертируем изначальную коллекцию в простую (массив товаров)
                // console.log('filter-by-price PurchasesStore.collection', PurchasesStore.collection);
                var initial_collection = Methods.convertPurchasesToFlatProducts(PurchasesStore.collection);
                // console.log('filter-by-price initial_collection', initial_collection);
                // console.log('filter-by-price PurchasesStore.categories', PurchasesStore.categories);
                var result = FilterFunctions.filterFlow(PurchasesStore.filter, initial_collection, PurchasesStore.categories);
                // console.log('filter-by-price result', result);
                PurchasesStore.filter.filtered_collection = result;
                PurchasesStore.filterTrigger();
            };            
            break;

        case 'view-by':
            PurchasesStore.view_state.view_by = payload.parametr;
            PurchasesStore.changeViewState();
            break;  

        case 'set-view-page':
            PurchasesStore.view_state.view_page = payload.view_page;
            PurchasesStore.changeViewState();
            break; 

        default:
            console.log('default dispatcher');
    };
    return true;

});


module.exports = PurchasesStore;
