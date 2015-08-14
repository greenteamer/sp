var SliderProducts = require('./product_components/SliderProducts.jsx');


var Catalog = React.createClass({displayName: "Catalog",
    render: function () {
        return (
            React.createElement("div", {className: "catalog"}, 
                React.createElement(SliderProducts, {items: this.props.catalog.products, cpp_catalog: this.props.catalog.cpp_catalog})
            )
        )
    }
});


var Catalogs = React.createClass({displayName: "Catalogs",
    render: function () {        
        items = this.props.catalogs.map(function(item, index){
            if (index === 0) {
                return (
                    React.createElement(Catalog, {key: item.id, catalog: item})
                )
            }
        });
        return (
            React.createElement("div", {className: "catalogs"}, 
                items
            )
        )
    }
});


module.exports = Catalogs;