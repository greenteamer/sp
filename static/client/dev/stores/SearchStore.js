var PurchasesDispatcher = require('../dispatcher/PurchasesDispatcher.js');
var SearchActions = require('../actions/SearchActions.js');
var MicroEvent = require('microevent');
var merge = require('merge');
var $ = require('jquery');
var _ = require('underscore');
var Cookies = require('js-cookie');
var snackbar = require('../../lib/snackbar.js');

// var Methods = require('../views/customhelpers/Methods.js');
// var FilterFunctions = require('../views/customhelpers/FilterFunctions.js');


var SearchStore = merge(MicroEvent.prototype, {
    
    // состояние поиска приложения
    search: {
        search_state: {
            query: ''
        },
        search_collection: []
    },
    searchStateTrigger : function () {
        console.log('Store searchStateTrigger start');
        this.trigger('searchStateTrigger');    
    },



    search_result_collection: [],
    query_text: '',
    searchResult: function () {
        console.log('Store searchResult start');
        this.trigger('searchResult');  
    },

});


PurchasesDispatcher.register(function (payload) {
    switch (payload.actionType) {

        case 'cahnge-search-state':
            // var result = get_search_result_purchases(payload.query);
            console.log('SearchStore cahnge-search-state: ');
            SearchStore.search.search_state.query = payload.query;
            SearchStore.searchStateTrigger();
            break;        

        default:
            console.log('default dispatcher');
    };
    return true;

});


module.exports = SearchStore;
