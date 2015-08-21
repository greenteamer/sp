var React = require('react');
var Catalogs = require('./Catalogs.jsx');
var PurchasesActions = require('../actions/PurchasesActions.js');


var ProductFastView = React.createClass({
    render: function(){
        return (
            <div className="product_view hidden">
                <h4>{this.props.product.name}</h4>
                <img src={this.props.product.image} alt="" />
                <p>{this.props.product.description}</p>
                <p>{this.props.product.price}</p>
            </div>
        )
    }
});


var Purchase = React.createClass({
    getInitialState: function(){
        return {
            product_fast_view: {
                name: 'Тест Имя',
                image: 'http://127.0.0.1:8000/media/product/5_4.png',
                description: 'Тест описание товара для быстрого просмотра',
                price: 1200
            }
        }
    },
    render: function () {
        var description = this.props.purchase.description.slice(0,100);
        description = description.replace(/(<([^>]+)>)/ig,"");
        return (
            <div className="purchase-item">
                <div className="row">
                    <div className="col-xs-12 col-md-4 purchase-info">
                        <h2>{this.props.purchase.name}</h2>
                        <p>{description}</p>
                    </div>
                    <div className="col-xs-12 col-md-8 purchase-info">
                        <Catalogs catalogs={this.props.purchase.catalogs} />
                    </div>
                    <ProductFastView product={this.state.product_fast_view}></ProductFastView>
                </div>
            </div>
        )
    }
});


var Purchases = React.createClass({
    render: function () {
        var length = this.props.collection.length;
        var items = this.props.collection.map(function (item, index){
            if (index === length-1) {
                return (
                    <div>
                        <Purchase key={item.id} purchase={item}/>
                    </div>
                )
                }
            else {
                return (
                    <div>
                        <Purchase key={item.id} purchase={item}/>
                        <div className="separator"></div>
                    </div>
                )
            }
        });
        return (
            <div className="purchases-list">
                {items}
            </div>
        )
    }
});


module.exports = Purchases;
