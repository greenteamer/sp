var React = require('react');
var $ = require('jquery');
var _ = require('underscore');
var ProductDetailView = require('../product_components/ProductDetailView.jsx');

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
            purchase: [],
            organizers: [],
            user: {},
            is_owner: false
        };
    },
    componentWillMount: function  () {        
        // получаем текущий урл и достаем из него id закупки
        var id = location.pathname.slice(-2,-1);                
        PurchasesActions.getCurrentPurchaseDetail(id);        
        FaqActions.getCurrentUser();
        PurchasesActions.setViewPage('purchase');
        PurchasesActions.getOrganizers();

        PurchasesStore.bind('chengePurchaseDetail', this.chengePurchase);
        PurchasesStore.bind('organizersTrigger', this.changeOrganizers);
        FaqStore.bind( 'change', this.userChanged );   
    },
    componentWillUnmount: function  () {        
        PurchasesStore.unbind('chengePurchaseDetail', this.chengePurchase);
        PurchasesStore.unbind('organizersTrigger', this.changeOrganizers);
        FaqStore.unbind( 'change', this.userChanged );
    },
    chengePurchase: function  () {
        this.setState({
            purchase: PurchasesStore.purchase
        });  
    },
    changeOrganizers: function () {
        // при получении всех профайлов находим профайл текущего пользователя state.user        
        tmp_user = this.state.user;
        console.log('organizer_profiles: ', PurchasesStore.organizer_profiles); 
        tmp_profile = _.find(PurchasesStore.organizer_profiles, function (profile) {
            console.log('profile in organizer_profiles: ', profile);    
            return profile.user = tmp_user.id;
        });
        // 
        tmp_this_purchase = this.state.purchase[0];
        console.log('find profile in organizer_profiles: ', tmp_profile);
        var check = _.some(tmp_profile.purchases, function (purchase) {
            // проходимя по всем его закупкам (tmp_profile.purchases) и возвращяем true в check если id текущей закупки хоть однажды совпадет с id одной из его закупок
            return purchase.id == tmp_this_purchase.id;
        });

        // меняем состояние компонента
        console.log('is_owner: ', check);
        this.setState({
            organizers: PurchasesStore.organizer_profiles,
            is_owner: check
        });

    },
    userChanged: function () {
        this.setState({
            user: FaqStore.user
        });                 
    },
    render: function () {
        console.log('PurchaseDetail render user: ', this.state.user);
        var left = $('.container').width()/2;
        if (this.state.purchase.length > 0) {
            return (
                <div>                    
                    <Purchases collection={this.state.purchase} view_state={this.state.view_state}/>
                    <h2>Комментарии</h2>
                    <FAQ 
                        purchase={this.state.purchase[0]}
                        product={null}
                        user={this.state.user}
                        is_owner={this.state.is_owner}/>
                </div>
            );
            
        } else {
            return (
                <div>                    
                    <RefreshIndicator size={40} left={left} top={5} status="loading" />
                </div>  
            );
        }
    }
});



module.exports = PurchaseView;
