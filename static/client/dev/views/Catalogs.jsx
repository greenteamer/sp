var React = require('react');
var SliderProducts = require('./product_components/SliderProducts.jsx');


var Catalog = React.createClass({
    render: function () {
        return (
            <div className="catalog">
                <SliderProducts 
                    items={this.props.catalog.product_catalog} 
                    cpp_catalog={this.props.catalog.cpp_catalog} 
                    purchase_id={this.props.purchase_id}
                    view_state={this.props.view_state}/>
            </div>
        )
    }
});


var Catalogs = React.createClass({
    render: function () {
        var purchase_id = this.props.purchase_id;
        var tmp_view_state = this.props.view_state;
        items = this.props.catalogs.map(function(item, index){
            if (index === 0) {
                return (
                    <Catalog 
                        key={item.id} 
                        catalog={item} 
                        purchase_id={purchase_id} 
                        view_state={tmp_view_state}/>
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
