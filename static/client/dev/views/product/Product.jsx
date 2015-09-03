var React = require('react');
var $ = require('jquery');
var ProductDetailView = require('../product_components/ProductDetailView.jsx');
var PurchasesStore = require('../../stores/PurchasesStore.js');
var PurchasesActions = require('../../actions/PurchasesActions.js');


function emptyObject(obj) {
    //вспомогательная функция проверяет пуст ли объект
    for (var i in obj) {
        return false;
    }
    return true;
}


var Product = React.createClass({
	getInitialState: function () {
        return {
            product: {},
          	user: {}
        }
    },
    componentWillMount: function () {
        //получаем текущий урл
        var url = $(location).attr('pathname');
        var product_id = url.split('/')[2];        
        //обновляем store в соответствии с текущей категорией
        PurchasesActions.getProduct(product_id);
        PurchasesStore.bind( 'get-product', this.collectionChanged );
    },
    componentWillUnmount: function () {
        PurchasesStore.unbind( 'get-product', this.collectionChanged );
    },
    collectionChanged: function () {
        this.setState({
            product: PurchasesStore.product,
            user: {}
        });
    },
	render: function () {
        if (!emptyObject(this.state.product)){
            return (
                <div>
                    <ProductDetailView  product={this.state.product}/>
                </div>
            )
        } else {
            return (
                <div></div>
            )
        }
	}
});


module.exports = Product;
