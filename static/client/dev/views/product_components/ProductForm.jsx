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

        console.log('ProductForm getInitialState props.cpp_catalog', this.props.cpp_catalog);
        console.log('ProductForm getInitialState props.product', this.props.product);

        var cpp_properties = [];
        this.props.cpp_catalog.forEach(function(cpp_property){
            cpp_properties.push({
                name: cpp_property.cpp_name,
                value: undefined,
                properties: cpp_property.cpp_values
            });
        });

        var product = this.props.product;
        product.count = 1;
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
    setCount: function(e){
        var new_product = this.state.product;
        new_product.count = e.target.value;
        this.setState({
            cpp_properties: this.state.cpp_properties,
            product: new_product
        });
    },
    countMinus: function(){
        var new_product = this.state.product;
        if (new_product.count > 1) {
            new_product.count = new_product.count - 1;
            this.setState({
                cpp_properties: this.state.cpp_properties,
                product: new_product
            });
        }
    },
    countPlus: function(){
        var new_product = this.state.product;
        new_product.count = new_product.count + 1;
        this.setState({
            cpp_properties: this.state.cpp_properties,
            product: new_product
        });
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
            var options = [];

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
                <div className="count_block">
                    <button type="button" className="btn btn-default pull-left minus" onClick={this.countMinus}>-</button>
                    <input
                        type="text"
                        name="count"
                        className="count_input"
                        onChange={this.setCount}
                        value={this.state.product.count}/>
                    <button type="button" className="btn btn-default pull-left plus" onClick={this.countPlus}>+</button>
                </div>
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
