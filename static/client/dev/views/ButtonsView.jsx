var React = require('react');
var PurchasesActions = require('../actions/PurchasesActions.js');
var PurchasesStore = require('../stores/PurchasesStore.js');

//material-ui
var mui = require('material-ui');
var IconButton = mui.IconButton;

var IF = require('./customhelpers/IF.jsx');


var ButtonsView = React.createClass({
    getInitialState: function () {
        return {
            view_state: PurchasesStore.view_state
        }  
    },
    componentWillMount: function  () {
        PurchasesStore.bind('changeViewState', this.changeViewState);    
    },
    componentWillUnmount: function  () {
        PurchasesStore.unbind('changeViewState', this.changeViewState);    
    },
    changeViewState: function  () {
        this.setState({
            view_state: PurchasesStore.view_state          
        });
    },
    changeViewToList: function(){
        PurchasesActions.changeViewType('list');        
    },
    changeViewToTite: function(){
        PurchasesActions.changeViewType('tile');
    },
    viewByProducts: function  () {
        PurchasesActions.viewBy('products');  
    },
    viewByPurchases: function  () {
        PurchasesActions.viewBy('purchases');    
    },
    render: function () {
        var button_style = {
            background: "#FFC229",
            width: "36px",
            height: "30px",
            padding: "0px",
            margin: "0 1px",
            top: "0px",
            borderRadius: "2px",
            textTransform: "uppercase"
        };
        var text_button_style = {
            background: "#FFC229",
            borderRadius: "2px",
            fontSize: "15px",
            width: "initial",
            height: "30px",
            padding: "0 10px",
            margin: "5px 1px",
            top: "0px",
            color: "#fff",            
            textTransform: "uppercase"
        };
        return (
            <div className="swich-view">
                <IF condition={this.state.view_state.view_by == 'products'}>                        
                    <IconButton
                            className="btn btn-primary"
                            onClick={this.viewByPurchases}                                   
                            tooltipPosition="top-center"
                            tooltip="Вывести товары по закупкам"
                            style={text_button_style}
                            iconStyle={{
                                color: "#fff"                                        
                            }}>
                        по закупкам
                    </IconButton>
                </IF>
                <IF condition={this.state.view_state.view_by != 'products'}>
                    <div>   
                        <IconButton
                                className="btn btn-primary"
                                onClick={this.viewByProducts}                                    
                                tooltipPosition="top-center"
                                tooltip="Вывести только продукты"
                                style={text_button_style}
                                iconStyle={{
                                    color: "#fff"                                        
                                }}>
                            по продуктам
                        </IconButton>
                        <IconButton
                                className="btn btn-primary"
                                onClick={this.changeViewToList}
                                iconClassName="material-icons"
                                tooltipPosition="top-center"
                                tooltip="Отобразить в виде сладера"
                                style={button_style}
                                iconStyle={{
                                    color: "#fff"
                                }}>
                            view_list
                        </IconButton>
                        <IconButton
                                className="btn btn-primary"
                                onClick={this.changeViewToTite}
                                iconClassName="material-icons"
                                tooltipPosition="top-center"
                                tooltip="Отобразить все товары"
                                style={button_style}
                                iconStyle={{
                                    color: "#fff"
                                }}>
                            view_module
                        </IconButton>                                                 
                    </div>
                </IF>
            </div>
        )
    }
});

module.exports = ButtonsView;