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
    }
};


module.exports = PurchasesActions;
