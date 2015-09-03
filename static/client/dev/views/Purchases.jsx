var React = require('react');
var $ = require('jquery');
var Catalogs = require('./Catalogs.jsx');
var PurchasesActions = require('../actions/PurchasesActions.js');
var PurchasesStore = require('../stores/PurchasesStore.js');
//var ProductForm = require('./product_components/ProductForm.jsx');
var ProductModal = require('./product_components/ProductModal.jsx');
var ProductTileView = require('./product_components/ProductTileView.jsx');
var PurchaseDetailInfo = require('./purchase/PurchaseDetailInfo.jsx');

//material-ui
var mui = require('material-ui');
var ThemeManager = require('material-ui/lib/styles/theme-manager')();


//my custom helpers
var IF = require('./customhelpers/IF.jsx');
var MyRefreshIndicator = require('./customhelpers/MyRefreshIndicator.jsx');


var CatalogTileView = React.createClass({
    render: function (){
        var tmp_cpp = this.props.catalog.cpp_catalog;
        var items = this.props.catalog.product_catalog.map(function(product){
            console.log(tmp_cpp);
            product.cpp_catalog = tmp_cpp;
            return (
                <div className="col-xs-12 col-sm-6 col-md-4">
                    <ProductTileView product={product}/>
                </div>
            )
        });
        return (
            <div className="row">
                <div className="col-xs-12">
                    <h5>Каталог: {this.props.catalog.catalog_name}</h5>
                </div>
                {items}
            </div>
        )
    }
});


var PurchaseTileView = React.createClass({
    getInitialState: function  () {
        return {
            view_state: PurchasesStore.view_state
        }  
    },
    render: function(){
        var items = this.props.purchase.catalogs.map(function(catalog){
            return (<CatalogTileView catalog={catalog}/>);
        });
        var link = "/purchases/" + this.props.purchase.id + "/";
        var condition = this.state.view_state.view_width === 9;
        return (
            <div className="purchase_tile_view">
                <div className="row">
                    <div className="col-xs-4">
                        <div className="purchase_tile_title">
                            <IF condition={condition}>
                                <PurchaseDetailInfo purchase={this.props.purchase} />
                            </IF>
                            <IF condition={!condition}>
                                <div>
                                    <h2 className="tile_view">{this.props.purchase.name}</h2>
                                    <a className="btn btn-primary purchase_link" href={link}>подробнее о закупке</a>
                                </div>
                            </IF>
                        </div>
                    </div>
                    <div className="col-xs-8">
                        {items}
                    </div>
                </div>                
            </div>
        )        
    }
});


var PurchaseListView = React.createClass({
    getInitialState: function  () {
        return {
            view_state: PurchasesStore.view_state
        }  
    },
    render: function () {
        var link = "/purchases/" + this.props.purchase.id + "/";
        var condition = this.state.view_state.view_width === 9;                
        return (
            <div className="purchase-item">
                <div className="row">
                    <div className="col-xs-12 col-md-4 purchase-info">
                        <IF condition={condition}>
                            <PurchaseDetailInfo purchase={this.props.purchase} />
                        </IF>
                        <IF condition={!condition}>
                            <div> 
                                <h2>{this.props.purchase.name}</h2>                             
                                <a className="btn btn-primary purchase_link" href={link}>подробнее о закупке</a>
                            </div>
                        </IF>
                    </div>
                    <div className="col-xs-12 col-md-8 purchase-info">
                        <Catalogs catalogs={this.props.purchase.catalogs} purchase_id={this.props.purchase.id} />
                    </div>
                </div>
            </div>
        )

    }
});


var Purchases = React.createClass({
    childContextTypes: {
        muiTheme: React.PropTypes.object
    },
    getChildContext: function() {
        return {
            muiTheme: ThemeManager.getCurrentTheme()
        };
    },
    getInitialState: function(){
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

        var items = this.props.collection.map(function (item, index) {            
            return (
                <div>
                    <IF condition={condition == true}>
                        <PurchaseListView key={item.id} purchase={item}/>
                    </IF>
                    <IF condition={condition == false}>
                        <PurchaseTileView key={item.id} purchase={item}/>
                    </IF>                   
                    <IF condition={index != length - 1}>
                        <div className='separator'></div>
                    </IF>                          
                </div>
            )
        });

        return (
            <div className="purchases-list">
                <div className="swich-view">
                    <button onClick={this.changeViewToList} type="button" className="btn btn-primary">
                        <i className="mdi-action-view-list"></i>
                    </button>
                    <button onClick={this.changeViewToTite} type="button" className="btn btn-primary">
                        <i className="mdi-action-view-module"></i>
                    </button>
                </div>
                <IF condition={length == 0}>
                    <MyRefreshIndicator relative_element_name={this.props.indicatorElementName} />
                </IF>
                {items}
                <ProductModal />
            </div>
        )

    }
});


module.exports = Purchases;
