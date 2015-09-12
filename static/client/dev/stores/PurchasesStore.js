var PurchasesDispatcher = require('../dispatcher/PurchasesDispatcher.js');
var PurchasesActions = require('../actions/PurchasesActions.js');
var MicroEvent = require('microevent');
var merge = require('merge');
var $ = require('jquery');
var _ = require('underscore');
var Cookies = require('js-cookie');
var snackbar = require('../../lib/snackbar.js');

var Methods = require('../views/customhelpers/Methods.js');


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

    // filter
    filter: {
        filtered_collection: []
    },
    filterTrigger : function () {
        this.trigger('filterTrigger');    
    },

    user: {},
    collection: [],
    cartitems: [],
    search_result_collection: [],
    query_text: '',

    product_fast_view: {},
    purchase_id_fast_view: 0,
    product: {},
    benefits: [],
    modal_photo: {},
    photoView: function(){
        console.log('start trigger photoView');
        this.trigger('photoView');
    },

    // for purchase page
    purchase: [],

    
    collectionChange: function(){
        this.trigger('change');
    },
    modalView: function(){
        this.trigger('modal');
    },
    getProduct: function(){
        this.trigger('get-product');
    },
    changeBenefits: function(){
        this.trigger('changeBenefits');
    },
    chengePurchaseDetail: function  () {
        this.trigger('chengePurchaseDetail');
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
                    console.log(PurchasesStore.collection);
                    PurchasesStore.collection[0].promo_purchase = data;
                    PurchasesStore.collection[0].name = "Горящие закупки";
                    console.log(PurchasesStore.collection);
                    PurchasesStore.collectionChange();

                }).bind(this),
                error: (function (xhr, status, err) {
                    console.log('error fetchin collection');
                }).bind(this)
            });
            break;

        case 'get-search-results':
            $.ajax({
                url: '/api/v1/search/purchases/' + '?query=' + payload.query,
                dataType: 'json',
                cache: false,
                success: (function (data) {
                    PurchasesStore.search_result_collection = data;
                    PurchasesStore.query_text = payload.query;
                    PurchasesStore.collectionChange();
                }).bind(this),
                error: (function (xhr, status, err) {
                    console.log('error fetchin collection');
                }).bind(this)
            });
            break;

        case 'add-to-cart':
            console.log('ajax start');
            var csrftoken = Cookies.get('csrftoken');
            var tmp_properties = '';
            payload.item.cpp_properties.forEach(function (property, index){
                if (index != 0) {
                    tmp_properties = tmp_properties + ',' + payload.item.cpp_properties[index].value;
                } else {
                    tmp_properties = payload.item.cpp_properties[index].value;
                }
            });
            console.log(tmp_properties);
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

        case "fast-show-product":
            //передаем продукт которй быстро хочет посмотреть человек
            PurchasesStore.product_fast_view = payload.product;
            PurchasesStore.product_fast_view.cpp_catalog = payload.cpp_catalog;
            PurchasesStore.purchase_id_fast_view = payload.purchase_id;
            PurchasesStore.modalView();
            break;

        case "show-photo":
            PurchasesStore.modal_photo = payload.photo;
            PurchasesStore.photoView();
            console.log("PurchasesStore.modal_photo: ", PurchasesStore.modal_photo);
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

        case 'get-current-purchase-datail':
            var url = '/api/v1/purchases/' + payload.id + '/'
            $.ajax({
                url: url,
                dataType: 'json',
                cache: false,
                success: (function(data){                    
                    PurchasesStore.purchase = [];
                    PurchasesStore.purchase.push(data);
                    PurchasesStore.chengePurchaseDetail();
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

        case 'view-by':
            PurchasesStore.view_state.view_by = payload.parametr;
            PurchasesStore.changeViewState();
            console.log('Dispatcher view-by PurchasesStore.filter.view_by : ', PurchasesStore.view_state.view_by);
            break;  

        case 'set-view-page':
            PurchasesStore.view_state.view_page = payload.view_page
            PurchasesStore.changeViewState();
            break; 

        default:
            console.log('default dispatcher');
    };
    return true;

});


module.exports = PurchasesStore;
