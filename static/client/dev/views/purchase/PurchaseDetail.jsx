var React = require('react');
var $ = require('jquery');
var ProductDetailView = require('../product_components/ProductDetailView.jsx');
var PurchasesStore = require('../../stores/PurchasesStore.js');
var PurchasesActions = require('../../actions/PurchasesActions.js');
var Catalogs = require('../Catalogs.jsx');
var Purchases = require('../Purchases.jsx');

//material-ui
var mui = require('material-ui');
var ThemeManager = require('material-ui/lib/styles/theme-manager')();
var RefreshIndicator = mui.RefreshIndicator;


var PurchaseView = React.createClass({
    childContextTypes: {
        muiTheme: React.PropTypes.object
    },
    getChildContext: function() {
        return {
            muiTheme: ThemeManager.getCurrentTheme()
        };
    },
    getInitialState: function  () {
        return {
            view_state: PurchasesStore.view_state,
            purchase: []
        }  
    },
    componentWillMount: function  () {        
        // получаем текущий урл и достаем из него id закупки
        var id = location.pathname.slice(-2,-1);        
        PurchasesActions.getCurrentPurchaseDetail(id);
        // изменяем ширину отображения на 9
        PurchasesActions.setViewPage('purchase');
        PurchasesStore.bind('chengePurchaseDetail', this.chengePurchase);
    },
    componentWillUnmount: function  () {        
        PurchasesStore.unbind('chengePurchaseDetail', this.chengePurchase);
    },
    chengePurchase: function  () {
        this.setState({
            purchase: PurchasesStore.purchase
        });  
    },
    render: function () {
        var left = $('.container').width()/2;
        if (this.state.purchase.length > 0) {
            return (                
                <Purchases collection={this.state.purchase} view_state={this.state.view_state}/>
            )
            
        } else {
            return (
                <div>                    
                    <RefreshIndicator size={40} left={left} top={5} status="loading" />
                </div>  
            )
        }
    }
});



module.exports = PurchaseView;
