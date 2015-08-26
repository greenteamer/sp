var React = require('react');
var SliderProducts = require('./product_components/SliderProducts.jsx');


var Catalog = React.createClass({
    render: function () {
        return (
            <div className="catalog">
                <SliderProducts items={this.props.catalog.product_catalog} cpp_catalog={this.props.catalog.cpp_catalog} purchase_id={this.props.purchase_id}/>
            </div>
        )
    }
});


var Catalogs = React.createClass({
    render: function () {
        var purchase_id = this.props.purchase_id;
        items = this.props.catalogs.map(function(item, index){
            if (index === 0) {
                return (
                    <Catalog key={item.id} catalog={item} purchase_id={purchase_id} />
                )
            }
        });
        return (
            <div className="catalogs">
                {items}
            </div>
        )
    }
});


module.exports = Catalogs;
