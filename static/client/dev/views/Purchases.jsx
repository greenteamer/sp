var React = require('react');
var $ = require('jquery');
var _ = require('underscore');
var Catalogs = require('./Catalogs.jsx');
var PurchasesActions = require('../actions/PurchasesActions.js');
var PurchasesStore = require('../stores/PurchasesStore.js');
var ButtonsView = require('./ButtonsView.jsx');
var ProductModal = require('./product_components/ProductModal.jsx');
var ProductHoverTitle = require('./product_components/ProductHoverTitle.jsx');
var ProductRelativeTitle = require('./product_components/ProductRelativeTitle.jsx');
var PurchaseDetailInfo = require('./purchase/PurchaseDetailInfo.jsx');

//material-ui
var mui = require('material-ui');
var IconButton = mui.IconButton;
var ThemeManager = require('material-ui/lib/styles/theme-manager')();


//my custom helpers
var IF = require('./customhelpers/IF.jsx');
var MyRefreshIndicator = require('./customhelpers/MyRefreshIndicator.jsx');
var Methods = require('./customhelpers/Methods.js');


var CatalogTileView = React.createClass({    
    render: function (){
        // Устанавливаем классы для каждого товара в зависимости от view_state.view_page
        // Получаем view_state из PurchaseTileView
        var products_class = '';
        if (this.props.view_state.view_page == 'purchase') {
            products_class = "col-xs-12 col-sm-4 col-md-3";
        } else {
            products_class = "col-xs-12 col-sm-6 col-md-4";
        } 
        
        var tmp_cpp = this.props.catalog.cpp_catalog;
        var tmp_view_state = this.props.view_state;
        
        var items = this.props.catalog.product_catalog.map(function(product){
            console.log(tmp_cpp);
            product.cpp_catalog = tmp_cpp;
            return (
                <div className={products_class}>
                    <IF condition={tmp_view_state.view_page != 'category'}>
                        <ProductHoverTitle product={product}/>
                    </IF>
                    <IF condition={tmp_view_state.view_page == 'category'}>
                        <ProductRelativeTitle product={product}/>
                    </IF>
                </div>
            );
        });
        return (
            <div className="row">
                <div className="col-xs-12">
                    <h5>Каталог: {this.props.catalog.catalog_name}</h5>
                </div>
                {items}
            </div>
        );
    }
});


var PurchaseTileView = React.createClass({
    render: function(){
        // Устанавливаем классы для каждой закупки в зависимости от view_state.view_page
        // Получаем view_state из Purchases
        var info_class = '';
        var products_class = '';
        if (this.props.view_state.view_page == 'purchase') {
            info_class = "col-xs-12 col-md-12";
            products_class = "col-xs-12 col-md-12";
        } else {
            info_class = "col-xs-12 col-md-4";
            products_class = "col-xs-12 col-md-8";
        } 

        var tmp_view_state = this.props.view_state;
        var items = this.props.purchase.catalogs.map(function(catalog){
            return (
                <CatalogTileView 
                    catalog={catalog}
                    view_state={tmp_view_state}/>
            );
        });

        var link = "/purchases/" + this.props.purchase.id + "/";        
        return (
            <div className="purchase_tile_view">
                <div className="row">
                    <div className={info_class}>
                        <div className="purchase_tile_title">
                            <IF condition={this.props.view_state.view_page == 'purchase'}>
                                <PurchaseDetailInfo 
                                    purchase={this.props.purchase}
                                    view_state={this.props.view_state}/>
                            </IF>
                            <IF condition={this.props.view_state.view_page != 'purchase'}>
                                <div>
                                    <h2 className="tile_view">{this.props.purchase.name}</h2>
                                    <a className="btn btn-primary purchase_link" href={link}>подробнее о закупке</a>
                                </div>
                            </IF>
                        </div>
                    </div>
                    <div className={products_class}>
                        {items}
                    </div>
                </div>                
            </div>
        );
    }
});


var PurchaseListView = React.createClass({
    render: function () {     
        // Устанавливаем классы для каждой закупки в зависимости от view_state.view_page
        // Получаем view_state из purchases
        var info_class = '';
        var products_class = '';
        if (this.props.view_state.view_page == 'purchase') {
            info_class = "col-xs-12 col-md-12 purchase-info";
            products_class = "col-xs-12 col-md-12 purchase-info";
        } else {
            info_class = "col-xs-12 col-md-4 purchase-info";
            products_class = "col-xs-12 col-md-8 purchase-info";
        }    
        return (
            <div className="purchase-item">
                <div className="row">
                    <div className={info_class}>                        
                        <PurchaseDetailInfo 
                            purchase={this.props.purchase} 
                            view_state={this.props.view_state}/>
                    </div>
                    <div className={products_class}>
                        <Catalogs 
                            catalogs={this.props.purchase.catalogs} 
                            purchase_id={this.props.purchase.id} 
                            view_state={this.props.view_state}/>
                    </div>
                </div>
            </div>
        );

    }
});


var Purchases = React.createClass({
    getInitialState: function(){
        return {
            view_state: PurchasesStore.view_state
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
    render: function () {        
        // Cоздаем условие при котором будет выводитсья PurchaseListView
        // state.view_state.view_type слушает Store
        // Компонент использует IF Helper из customhelpers (смотри описание внутри файла IF.jsx)
        // items - готовый список закупок
        // Компонент содержит кнопки переключения вида, состояние вида пишется в Store для глобального использования, затем меняется состояние компонента
        // condition index != length - 1 делается для вывода сепаратора, если закупка не последняя
        // MyRefreshIndicator ... relative_element_name - id или class эллемента относительно которого
        // мы расчитываем позицию индикатора

        var length = this.props.collection.length;
        var condition = this.state.view_state.view_type === 'list' || this.state.view_state.view_type === '';
        // var view_by_condition = this.state.view_state.view_by == 'products';
        var tmp_view_state = this.state.view_state;
        var items = this.props.collection.map(function (item, index) {            
            return (
                <div>
                    <IF condition={condition == true}>
                        <PurchaseListView 
                            key={item.id}
                            purchase={item}
                            view_state={tmp_view_state}/>
                    </IF>
                    <IF condition={condition == false}>
                        <PurchaseTileView 
                            key={item.id} 
                            purchase={item}
                            view_state={tmp_view_state}/>
                    </IF>                   
                    <IF condition={index != length - 1}>
                        <div className='separator'></div>
                    </IF>                          
                </div>
            );
        });

        var flat_products = Methods.convertPurchasesToFlatProducts(this.props.collection);
        flat_items = flat_products.map(function (product) {
            return (
                <div className="col-xs-12 col-sm-4 col-md-3 col-lg-3">
                    <ProductHoverTitle product={product}/>
                </div>
            );
        });

        console.log('Purchases state view_state: ', this.state.view_state);        
        return (
            <div className="purchases-list">
                <ButtonsView />
                <IF condition={this.props.collection.length == 0}>
                    <MyRefreshIndicator relative_element_name={this.props.indicatorElementName} />
                </IF>
                <IF condition={this.state.view_state.view_by != 'products'}>
                    <div>{items}</div>
                </IF>
                <IF condition={this.state.view_state.view_by == 'products'}>
                    <div className="row">{flat_items}</div>
                </IF>
                <ProductModal />
            </div>
        );

    }
});


module.exports = Purchases;
