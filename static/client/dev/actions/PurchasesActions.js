var PurchasesDispatcher = require('../dispatcher/PurchasesDispatcher.js');


var PurchasesActions = {
    getPopularPromo: function() {
        PurchasesDispatcher.dispatch({
            actionType: "get-popular-promo",
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
    getCartItems: function(){
        PurchasesDispatcher.dispatch({
            actionType: "get-cart-items"
        });
    },
    getSearchResults: function(query){
        PurchasesDispatcher.dispatch({
            actionType: "get-search-results",
            query: query
        });
    },
    fastShowProduct: function(data){
        PurchasesDispatcher.dispatch({
            actionType: "fast-show-product",
            product: data.item,
            purchase_id: data.purchase_id,
            cpp_catalog: data.cpp_catalog
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
    }
};


module.exports = PurchasesActions;
