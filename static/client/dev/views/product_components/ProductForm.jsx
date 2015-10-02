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
var FaqStore = require('../../faq/stores/FaqStore.js');
var RegisterModal = require('./RegisterModal.jsx');

var Methods = require('../customhelpers/Methods.js');
var IF = require('../customhelpers/IF.jsx');

var $ = require('jquery');
var _ = require('underscore');
var snackbar = require('../../../lib/snackbar.js');


var Properties = React.createClass({
    test: function () {
        
    },
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
        };
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
        // устанавливаем true в chacked если проверка успешна иначе false, undefined если не все параметры были выбраны
        // подобное описание метода chackProperties смотри внутри файла customhelpers/Methods.js
        // console.log('this.props.cpp_catalog: ', this.props.cpp_catalog);
        // console.log('this.state.cpp_properties: ', this.state.cpp_properties);
        this.setState({
            chacked: Methods.chackProperties(this.state.cpp_properties, this.props.product.property)
        }); 
        
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
    messageUser: function (){
        console.log('message user start');
        var message = {
            text: "Пройдите регистрацию чтобы заказать товары",
            link: "/profile/registration/"
        };
        PurchasesActions.showMessageModal(message);
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
            );
        });
        console.log('user: ', this.props.user);
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
                <IF condition={this.props.user}>
                    <button type="button" className="btn btn-primary full-width" onClick={this.addToCart}>В корзину</button>
                </IF>
                <IF condition={this.props.user == undefined}>
                    <button type="button" className="btn btn-primary full-width" onClick={this.messageUser}>В корзину</button>
                </IF>
                <RegisterModal/>
            </div>
        );
    }
});


var ProductForm = React.createClass({
  getInitialState: function () {
    console.log('ProductForm getInitialState start');
    return {
      user: undefined
    };
  },  
  componentWillMount: function () {
    console.log('ProductForm componentWillMount start');
    FaqStore.bind( 'change', this.userChanged );
  },
  componentWillUnmount: function () {
    FaqStore.unbind( 'change', this.userChanged );
  },
  userChanged: function () {
    this.setState({
      user: FaqStore.user
    });
  },
  render: function(){  
  console.log('ProductForm render start');
    return (
      <div className="properties">
        <input type="hidden" name="product" value={this.props.product.id} />
        <Properties 
          cpp_catalog={this.props.cpp_catalog} 
          product={this.props.product} 
          user={this.state.user}/>
      </div>
    );
  }
});


module.exports = ProductForm;
