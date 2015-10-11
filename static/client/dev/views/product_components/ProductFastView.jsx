var React = require('react');
var PurchasesActions = require('../../actions/PurchasesActions.js');
var PurchasesStore = require('../../stores/PurchasesStore.js');
var ProductForm = require('./ProductForm.jsx');
var FaqStore = require('../../faq/stores/FaqStore.js');
var FaqActions = require('../../faq/actions/FaqActions.js');


function emptyObject(obj) {
    //вспомогательная функция проверяет пуст ли объект
    for (var i in obj) {
        return false;
    }
    return true;
}


var ProductFastView = React.createClass({
  render: function(){
    var description = this.props.product.description;
    description = (description.substr(0, 500));
    console.log('ProductFastView render start');
    return (
      <div className="product_view">
        <div className="col-xs-12 col-sm-6 col-md-4 product_fast_view">
          <img src={this.props.product.images[0].image} alt="" />
        </div>
        <div className="col-xs-12 col-sm-6 col-md-8 product_fast_view">
          <div className="row">
            <div className="col-xs-12">
              <h2>{this.props.product.product_name}</h2>
            </div>
            <div className="col-xs-12 col-sm-12 col-md-6">
              <p>{description}</p>
            </div>
            <div className="col-xs-12 col-sm-12 col-md-6">
              <p className="price">{this.props.product.price} руб.</p>
            <ProductForm product={this.props.product} cpp_catalog={this.props.product.cpp_catalog}/>
              <a className="btn btn-default" href={'/products/'+this.props.product.id}>смотреть подробнее</a>
            </div>
            </div>
        </div>
      </div>
    );

  }
});


module.exports = ProductFastView;
