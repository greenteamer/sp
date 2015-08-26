var React = require('react');
var PurchasesActions = require('../../actions/PurchasesActions.js');
var PurchasesStore = require('../../stores/PurchasesStore.js');
var ProductDetailForm = require('./ProductDetailForm.jsx');
var Benefits = require('../Benefits.jsx');
var Tabs = require('material-ui').Tabs;
var Tab = require('material-ui').Tab;
var ThemeManager = require('material-ui/lib/styles/theme-manager')();
var Colors = require('material-ui').Styles.Colors;


function emptyObject(obj) {
    //вспомогательная функция проверяет пуст ли объект
    for (var i in obj) {
        return false;
    }
    return true;
}


var ProductFastView = React.createClass({
    childContextTypes: {
        muiTheme: React.PropTypes.object
    },
    getChildContext: function() {
        return {
            muiTheme: ThemeManager.getCurrentTheme()
        };
    },
    componentWillMount() {
        ThemeManager.setPalette({
           accent1Color: Colors.amber400
        });
    },
    render: function(){
        var description = this.props.product.description;
        description = (description.substr(0, 350));
        var tabsStyle = {
            'tabs': {
                'border': '1px solid #C5C5C5',
                'padding': '15px'},
            'tab': {
                'background': '#443f39'}
            };
        return (
            <div className="product_view">
                <div className="col-xs-12 col-sm-5 col-md-5 product_fast_view">
                    <img src={this.props.product.images[0].image} alt="" />
                </div>
                <div className="col-xs-12 col-sm-7 col-md-7 product_fast_view">
                    <div className="row">
                        <div className="col-xs-12">
                            <div className="row">
                                <div className="col-xs-12 col-sm-8 col-md-9">
                                    <h2>{this.props.product.product_name}</h2>
                                    <p>Артикул: <b>{this.props.product.sku}</b></p>
                                </div>
                                <div className="col-xs-12 col-sm-4 col-md-3">
                                    <p className="price">{this.props.product.price} руб.</p>
                                </div>
                            </div>
                        </div>
                        <div className="col-xs-12 col-sm-12 col-md-12">
                            <p>{description} ...</p>
                        </div>
                        <div className="col-xs-12 col-sm-12 col-md-12">
                            <ProductDetailForm product={this.props.product} cpp_catalog={this.props.product.cpp_catalog} />
                        </div>
                        <div className="col-xs-12 col-sm-12 col-md-12">
                            <Benefits />
                        </div>
                        <div className="col-xs-12 col-sm-12 col-md-12">
                            <div className="full-description">
                                <Tabs className="my_tabs" style={tabsStyle.tabs}>
                                    <Tab label="Описание" style={tabsStyle.tab}>
                                        <div>
                                            <h2>Описание</h2>
                                            <p>
                                                {this.props.product.description}
                                            </p>
                                        </div>
                                    </Tab>
                                    <Tab label="Комментарии" style={tabsStyle.tab}>
                                        <div>
                                            <h2>Комментарии</h2>
                                            <p>
                                                This is another example of a tab template!
                                            </p>
                                            <p>
                                                Fair warning - the next tab routes to home!
                                            </p>
                                        </div>
                                    </Tab>

                                </Tabs>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )

    }
});


module.exports = ProductFastView;
