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

var $ = require('jquery');
var _ = require('underscore');
var snackbar = require('../../../lib/snackbar.js');


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
        product.count = 1;
        return {
            cpp_properties: cpp_properties,
            product: product,
            chacked: false
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

        // РЕАЛИЗАЦИЯ ПРОВЕРКИ СУЩЕСТВОВАНИЯ КОМБИНАЦИИ СВОЙСТВ
        var properties_filled = _.every(this.state.cpp_properties,function (property) {
            // проверяем все ли свойства заполнены
            // _.every - возвращает true если все итерации функции вернули true
            return property.value != undefined;
        });        
        if (properties_filled) {
            var values_str = _.pluck(this.state.cpp_properties, 'value').join(',');
            // _.pluck - возвращает массив состоящий из значений полей 'value' объектов массива
            // join - создает из массива выбранных параметров строку параметров через ','
            if (_.contains(this.props.product.property.split(';'), values_str)) {
                // _.contains - возвращает true если массив содежит элемент values_str
                this.setState({
                    chacked: true
                });
            } else {
                this.setState({
                    chacked: false
                });
                $.snackbar({timeout: 5000, content: 'Нет товара с такими характеристиками, пожалуйста, попробуйте другие варианты' });
            }
        };        
        
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
        // если товар с такими свойствами существует добавляем товар в корзину
        if (this.state.chacked) {
            PurchasesActions.addToCart(this.state);
        } else {
            $.snackbar({timeout: 5000, content: 'Нет товара с такими характеристиками, пожалуйста, попробуйте другие варианты' });
        }
        
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
                <p>
                    <Select
                        name="property_value"
                        ref="my_select"
                        value={tmp_name}
                        options={options}
                        onChange={boundChange}
                         />
                </p>
            )
        });
        console.log('form is chacked: ', this.state.chacked);
        return (
            <div className="row">
                <div className="col-xs-12 col-sm-6">
                    {selects}
                </div>
                <div className="col-xs-12 col-sm-6">
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
            </div>
        )
    }
});


var ProductDetailForm = React.createClass({
    render: function(){        
        return (
            <div className="properties">
                <input type="hidden" name="product" value={this.props.product.id} />
                <Properties cpp_catalog={this.props.cpp_catalog} product={this.props.product}/>
            </div>
        )
    }
});


module.exports = ProductDetailForm;
