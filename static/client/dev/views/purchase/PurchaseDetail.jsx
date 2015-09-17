var React = require('react');
var $ = require('jquery');
var _ = require('underscore');
var ProductDetailView = require('../product_components/ProductDetailView.jsx');
var ProductRelativeTitle = require('../product_components/ProductRelativeTitle.jsx');
var ProductModal = require('../product_components/ProductModal.jsx');

// stores
var PurchasesStore = require('../../stores/PurchasesStore.js');
var FaqStore = require('../../faq/stores/FaqStore.js');

//actions
var FaqActions = require('../../faq/actions/FaqActions.js');
var PurchasesActions = require('../../actions/PurchasesActions.js');

var Catalogs = require('../Catalogs.jsx');
var Purchases = require('../Purchases.jsx');

// приложение FAQ переехало из proslavlenie.ru
var FAQ = require('../../faq/views/App.jsx');

//material-ui
var mui = require('material-ui');
var ThemeManager = require('material-ui/lib/styles/theme-manager')();
var RefreshIndicator = mui.RefreshIndicator;

var Methods = require('../customhelpers/Methods.js');
var IF = require('../customhelpers/IF.jsx');


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
            collection: [],
            filtered_collection: [],
            organizers: [],
            user: {},
            is_owner: false
        };
    },
    componentWillMount: function  () {        
        // test get category url
        var current_category = Methods.getCategorySlug();
        // console.log('PurcahseDetail current category slug: ', current_category);

        // получаем текущий урл и достаем из него id закупки
        var id = location.pathname.slice(-2,-1);                
        PurchasesActions.getCurrentPurchaseDetail(id);
        PurchasesActions.setViewPage('purchase');

        PurchasesStore.bind('chengePurchaseDetail', this.chengePurchase);        
        PurchasesStore.bind( 'change', this.collectionChanged ); 
        PurchasesStore.bind( 'filterTrigger', this.filterTrigger );  
    },
    componentWillUnmount: function  () {        
        PurchasesStore.unbind('chengePurchaseDetail', this.chengePurchase);
        PurchasesStore.unbind( 'change', this.collectionChanged );
        PurchasesStore.unbind( 'filterTrigger', this.filterTrigger );
    },
    collectionChanged: function () {
        this.setState({
            collection: PurchasesStore.collection
        });                 
    },
    filterTrigger: function () {
        this.setState({
            filtered_collection: PurchasesStore.filter.filtered_collection
        });
    },
    render: function () {
        // console.log('PurchaseDetail render filtered_collection.length: ', this.state.filtered_collection.length);
        var left = $('.container').width()/2;
        var filtered_items = []; 
        if (this.state.filtered_collection.length != 0){
            filtered_items = this.state.filtered_collection.map(function (product) {
                return (
                    <div className="col-xs-12 col-sm-4 col-md-3 col-lg-3">
                        <ProductRelativeTitle product={product}/>
                    </div>
                );
            });
        }   
        return (
            <div>
                <IF condition={this.state.filtered_collection.length == 0 && this.state.collection.length > 0}>
                    <div>                    
                        <Purchases collection={this.state.collection} view_state={this.state.view_state}/>
                        <h2>Комментарии</h2>
                    </div>
                </IF>                
                <IF condition={this.state.filtered_collection.length != 0}>
                    <div>
                        {filtered_items}
                        <ProductModal />
                    </div>                    
                </IF>
                <IF condition={this.state.collection.length == 0}>
                    <div>                    
                        <RefreshIndicator size={40} left={left} top={5} status="loading" />
                    </div>  
                </IF>    
            </div>
        );                    
    }
});



module.exports = PurchaseView;
