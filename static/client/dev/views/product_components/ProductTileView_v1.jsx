var React = require('react');
var PurchasesActions = require('../../actions/PurchasesActions.js');
var PurchasesStore = require('../../stores/PurchasesStore.js');
var ProductForm = require('./ProductForm.jsx');


function emptyObject(obj) {
    //вспомогательная функция проверяет пуст ли объект
    for (var i in obj) {
        return false;
    }
    return true;
}


var ProductTileView = React.createClass({
    showProduct: function(){
        var data = {
            item: this.props.product,
            //purchase_id: this.props.purchase_id,
            cpp_catalog: this.props.product.cpp_catalog
        };
        PurchasesActions.fastShowProduct(data);
    },
    render: function(){
        var description = this.props.product.description;
        description = (description.substr(0, 100));
        var link = "/client/products/" + this.props.product.id + "/";
        return (
            <div className="product_view product_tile_view row">
                <div className="col-xs-12">
                    <div className="image_block">
                        <button type="button" className="btn btn-primary fast-modal left" onClick={this.showProduct}>
                            <i className="mdi-content-content-copy"></i>
                        </button>
                        <a href={link} className="btn btn-primary fast-modal right">
                            <i className="mdi-action-search"></i>
                        </a>
                        <img src={this.props.product.images[0].cropping_url} alt="" />
                        <div className="gradient"></div>
                    </div>
                </div>
                <div className="col-xs-12">
                    <div className="info">
                        <div className="info_inner">
                            <h3>{this.props.product.product_name}</h3>
                            <p className="price">{this.props.product.price} руб.</p>
                        </div>
                    </div>
                    <ProductForm product={this.props.product} cpp_catalog={this.props.product.cpp_catalog} />
                </div>
            </div>
        )

    }
});


module.exports = ProductTileView;