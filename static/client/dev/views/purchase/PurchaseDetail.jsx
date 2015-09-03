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


function emptyObject(obj) {
    //вспомогательная функция проверяет пуст ли объект
    for (var i in obj) {
        return false;
    }
    return true;
}


var PurchaseDetail = React.createClass({
    render: function () {
        var description = this.props.purchase.description.slice(0,100);
        description = description.replace(/(<([^>]+)>)/ig,"");
        var link = "/client/purchases/" + this.props.purchase.id + "/";
        return (
            <div className="purchase-item">
                <div className="row">
                    <div className="col-xs-12 col-md-4 purchase-info">
                        <h2>{this.props.purchase.name}</h2>
                        <p>{description}</p>
                        <a className="btn btn-primary purchase_link" href={link}>подробнее о закупке</a>
                    </div>
                    <div className="col-xs-12 col-md-8 purchase-info">
                        <Catalogs catalogs={this.props.purchase.catalogs} purchase_id={this.props.purchase.id} />
                    </div>
                    <div className="col-xs-12">
                        <div className="row fast-open out">
                        </div>
                    </div>
                </div>
            </div>
        )
    }
});

    // render: function () {
    //     if (emptyObject(this.state.purchase)) {
    //         return (
    //             <div>
    //                 <h4>Эта закупка временно не доступна, попробуйте перезагрузить страницу пожзже</h4>
    //             </div>                
    //         )
            
    //     } else {
    //         return (
    //             <PurchaseDetail purchase={this.state.purchase} />
    //             <Purchases collection={collection} title={title}/>
    //         )
    //     }
    // }
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
        PurchasesActions.setViewStateWidth(9);
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
