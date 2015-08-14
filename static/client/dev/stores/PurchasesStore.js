var PurchasesDispatcher = require('../dispatcher/PurchasesDispatcher.js');
var MicroEvent = require('microevent');
var merge = require('merge');
var Cookies = require('js-cookie');


var PurchasesStore = merge(MicroEvent.prototype, {
    user: {},
    collection: [],

    collectionChange: function(){
        this.trigger('change');
    }
});


PurchasesDispatcher.register(function (payload) {
    switch (payload.actionType) {

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
                "/client/add-to-cart/",
                {
                    ajax: 'add_to_cart',
                    csrfmiddlewaretoken: csrftoken,
                    product: payload.item.product.id,
                    product_properties: tmp_properties,
                    quantity: '1'
                }
            ).success(
                function (data) {

                    for (var i = 0; i < FaqStore.collection.length; i++){
                        if (FaqStore.collection[i].id == data.question_id){
                            FaqStore.collection[i].answers.push({
                                photo: data.photo,
                                name: data.name,
                                date: data.date,
                                text: data.text
                            });
                            break
                        }
                    }

                    FaqStore.collectionChange();
                })
            .error(
                function (data) {
                    console.log("Ошибка post запроса");
                });
            break;

        default:
            console.log('default dispatcher');
    };
    return true;

});


module.exports = PurchasesStore;