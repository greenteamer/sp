
var Properties = React.createClass({displayName: "Properties",
    render: function(){
        // получаем свойства товара из общих возможных свойств каталога
        var cpp_catalog = this.props.cpp_catalog;
        var selects = cpp_catalog.map(function (select) {
            var opts = select.cpp_values.split(';');
            var options = opts.map(function(option){
                return (
                    React.createElement("option", {value: option}, option)
                );
            });
            return (
                React.createElement("select", null, 
                    options
                )
            )
        });

        return (
            React.createElement("div", null, 
                selects
            )
        )
    }
});


var ProductForm = React.createClass({displayName: "ProductForm",
    render: function(){        
        return (
            React.createElement("div", {className: "properties"}, 
                React.createElement("form", {action: ".", method: "post"}, 
                    React.createElement("input", {type: "hidden", name: "product", value: this.props.product.id}), 
                    React.createElement(Properties, {properties: this.props.product.property, cpp_catalog: this.props.cpp_catalog}), 
                    React.createElement("button", {type: "submit", className: "btn btn-primary full-width"}, "В корзину")
                )
            )
        )
    }
});


module.exports = ProductForm;