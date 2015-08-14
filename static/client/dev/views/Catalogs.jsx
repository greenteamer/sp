var React = require('react');
var SliderProducts = require('./product_components/SliderProducts.jsx');


var Catalog = React.createClass({
    render: function () {
        return (
            <div className="catalog">
                <SliderProducts items={this.props.catalog.products} cpp_catalog={this.props.catalog.cpp_catalog} />
            </div>
        )
    }
});


var Catalogs = React.createClass({
    render: function () {        
        items = this.props.catalogs.map(function(item, index){
            if (index === 0) {
                return (
                    <Catalog key={item.id} catalog={item} />
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
