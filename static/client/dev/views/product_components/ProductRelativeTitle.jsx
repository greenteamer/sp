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
        var link = "/products/" + this.props.product.id + "/";
        return (                        
            <div className="product_view image-wrapper product-relative-tittle row">
                <div className="col-xs-12">
                    <div className="image_block">                        
                        <a href={link} className="">
                            <img src={this.props.product.images[0].cropping_url} alt="" />
                        </a>
                        <div className="gradient"></div>
                    </div>
                </div>
                <div className="col-xs-12">
                    <h5 className="product_name_mini">{this.props.product.product_name}</h5>
                    <p className="price">{this.props.product.price}</p>                   
                </div>
                <div className="col-xs-12">
                    <button type="button" className="btn btn-primary full-width" onClick={this.showProduct}>
                        <i className="fa fa-shopping-cart"></i> в корзину
                    </button>
                </div>
            </div>
        )

    }
});


module.exports = ProductTileView;
