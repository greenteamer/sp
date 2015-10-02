var PurchasesDispatcher = require('../dispatcher/PurchasesDispatcher.js');


var PurchasesActions = {
    getPopularPromo: function() {
        PurchasesDispatcher.dispatch({
            actionType: "get-popular-promo",
        });
    },
    getInitialPurchases: function () {
        console.log('Actions get initial purchases start');
        PurchasesDispatcher.dispatch({
            actionType: "get-initial-purchases"
        });  
    },
    getNewPromo: function() {
        PurchasesDispatcher.dispatch({
            actionType: "get-new-promo",
        });
    },
    getHotPurchases: function() {
        PurchasesDispatcher.dispatch({
            actionType: "get-hot-purchases",
        });
    },
    addToCart: function(item) {
        PurchasesDispatcher.dispatch({
            actionType: "add-to-cart",
            item: item
        });
    },
    changeViewType: function(type) {
        PurchasesDispatcher.dispatch({
            actionType: "change-view-type",
            type: type
        });
    },
    //category
    getCategoryPurchases: function(category){
        PurchasesDispatcher.dispatch({
            actionType: "get-category-purchases",
            category: category
        });
    },
    getCategoriesTree: function () {
        PurchasesDispatcher.dispatch({
            actionType: "get-categories"
        });  
    },
    getCatalogs: function () {
        PurchasesDispatcher.dispatch({
            actionType: 'get-catalogs'
        });  
    },
    getCartItems: function(){
        PurchasesDispatcher.dispatch({
            actionType: "get-cart-items"
        });
    },
    getOrganizers: function () {
        PurchasesDispatcher.dispatch({
            actionType: "get-organizers"
        });
    },
    getSearchResults: function(query){
        PurchasesDispatcher.dispatch({
            actionType: "get-search-results",
            query: query
        });
    },
    fastShowProduct: function(data){
        console.log('PurchasesActions start fastShowProduct, data:', data);
        PurchasesDispatcher.dispatch({
            actionType: "fast-show-product",
            product: data.item,
            purchase_id: data.purchase_id,
            cpp_catalog: data.cpp_catalog
        });
    },
    showPhoto: function (photo) {
        PurchasesDispatcher.dispatch({
            actionType: "show-photo",
            photo: photo            
        }); 
    },
    showMessageModal: function (message) {
        console.log('PurchasesActions start showMessageModal, message:', message);
        PurchasesDispatcher.dispatch({
            actionType: "show-message-modal",
            message: message
        });
    },
    getProduct: function(product_id){
        PurchasesDispatcher.dispatch({
            actionType: "get-product",
            product_id: product_id
        });
    },
    getBenefits: function(){
        PurchasesDispatcher.dispatch({
            actionType: "get-benefits"
        });
    },
    getCurrentPurchaseDetail: function (id) {
        PurchasesDispatcher.dispatch({
            actionType: 'get-current-purchase-datail',
            id: id
        });
    },

    // ФИЛЬТРЫ, СОРТИРОВКИ, РЕЖИМЫ ОТОБРАЖЕНИЯ
    setViewStateWidth: function  (num) {
        PurchasesDispatcher.dispatch({
            actionType: 'set-view-width',
            num: num
        });
    },
    filterCollection: function(filtered_collection){
        PurchasesDispatcher.dispatch({
            actionType: 'filter-collection',
            filtered_collection: filtered_collection
        });  
    },

    filterByCategory: function (category_slug) {        
        // отправляем только slug
        PurchasesDispatcher.dispatch({
            actionType: 'filter-by-category',
            category_slug: category_slug
        });
    },
    filterByPrice: function (values) {        
        // отправляем только values
        PurchasesDispatcher.dispatch({
            actionType: 'filter-by-price',
            price: values
        });
    },
    viewBy: function (parametr) {
        PurchasesDispatcher.dispatch({
            actionType: 'view-by',
            parametr: parametr  
        });
    },
    setViewPage: function (view_page) {
        PurchasesDispatcher.dispatch({
            actionType: 'set-view-page',
            view_page: view_page
        });
    }
};


module.exports = PurchasesActions;
