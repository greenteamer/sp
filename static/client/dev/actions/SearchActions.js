var PurchasesDispatcher = require('../dispatcher/PurchasesDispatcher.js');


var SearchActions = {   
    changeSearchState: function (query) {
        console.log('SearchActions change search state start');
        PurchasesDispatcher.dispatch({
            actionType: 'cahnge-search-state',
            query: query
        });
    }
};


module.exports = SearchActions;
