var React = require('react');
var Select = require('react-select');
var ThemeManager = require('material-ui/lib/styles/theme-manager')();
var injectTapEventPlugin = require("react-tap-event-plugin");
var mui = require('material-ui');
    FlatButton = mui.FlatButton;
    SelectField = mui.SelectField;
    DropDownMenu = mui.DropDownMenu;
    TextField = mui.TextField;
var PurchasesActions = require('../../actions/PurchasesActions.js');


var Properties = React.createClass({
    getInitialState: function() {
        var cpp_properties = [];
        this.props.cpp_catalog.forEach(function(cpp_property){
            cpp_properties.push({
                name: cpp_property.cpp_name,
                value: undefined,
                properties: cpp_property.cpp_values
            });
        });

        var product = this.props.product;
        return {
            cpp_properties: cpp_properties,
            product: product
        }
    },
    childContextTypes: {
        muiTheme: React.PropTypes.object
    },
    getChildContext: function() {
        return {
            muiTheme: ThemeManager.getCurrentTheme()
        };
    },
    setProperties: function(val, e){
        //изменяем state когда выбирается какое либо свойство
        this.state.cpp_properties[e[0].index].value = e[0].value;
    },
    addToCart: function(e){
        //добавляем товар в корзину
        PurchasesActions.addToCart(this.state);
    },

    render: function(){
        // получаем свойства товара из общих возможных свойств каталога
        //var product = this.props.product;
        var boundChange = this.setProperties.bind(this);

        //проходимся по каждому свойству что бы сгенерировать select
        var selects = this.state.cpp_properties.map(function (select, index) {
            var opts = select.properties.split(';');
            var options = []

            //проходимя по каждому свойству и добавляем их в options select +
            //добавляем name для индексации select
            opts.forEach(function(opt){
                options.push({
                    value: opt,
                    label: opt,
                    index: index
                });
            });

            var tmp_name = select.value;
            if (tmp_name === undefined) {
                tmp_name = select.name;
            }

            return (
                <Select
                    name="property_value"
                    ref="my_select"
                    value={tmp_name}
                    options={options}
                    onChange={boundChange}
                     />
            )
        });

        return (
            <div>
                {selects}
                <button type="button" className="btn btn-primary full-width" onClick={this.addToCart}>В корзину</button>
            </div>
        )
    }
});


var ProductForm = React.createClass({
    render: function(){        
        return (
            <div className="properties">
                <input type="hidden" name="product" value={this.props.product.id} />
                <Properties cpp_catalog={this.props.cpp_catalog} product={this.props.product}/>
            </div>
        )
    }
});


module.exports = ProductForm;
