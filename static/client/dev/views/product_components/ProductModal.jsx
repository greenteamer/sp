var React = require('react');
var PurchasesActions = require('../../actions/PurchasesActions.js');
var PurchasesStore = require('../../stores/PurchasesStore.js');
var ProductForm = require('./ProductForm.jsx');
var ProductFastView = require('./ProductFastView.jsx');
var Dialog = require('material-ui').Dialog;
var ThemeManager = require('material-ui/lib/styles/theme-manager')();
var FlatButton = require('material-ui').FlatButton;
var Colors = require('material-ui').Styles.Colors;


function emptyObject(obj) {
    //вспомогательная функция проверяет пуст ли объект
    for (var i in obj) {
        return false;
    }
    return true;
}

var ProductModal = React.createClass({
    getInitialState: function(){
        return {
            product_fast_view: {},
            purchase_id_fast_view: 0
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
    componentDidMount: function () {
        PurchasesStore.bind( 'modal', this.collectionChanged );
    },
    componentWillUnmount: function () {
        PurchasesStore.unbind( 'modal', this.collectionChanged );
    },
    collectionChanged: function () {
        this.setState({
            product_fast_view: PurchasesStore.product_fast_view,
            purchase_id_fast_view: PurchasesStore.purchase_id_fast_view
        });
        this.state.product_fast_view = PurchasesStore.product_fast_view;
        if (emptyObject(this.state.product_fast_view) != true) {
            this.refs.productDialog.show();
        }
    },
    _DialogCancel: function () {
    	this.refs.productDialog.dismiss();
    },
    render: function(){
        var modalActions = [
			  <FlatButton
			    label="Закрыть"
			    secondary={true}
			    className="modal-button-cancel btn btn-default"
			    onClick={this._DialogCancel} />
        ];
        var productModal = [
            <Dialog
                ref="productDialog"
                className="test_modal"
                title="Быстрый просмотр товара"
                actions={modalActions}>
            </Dialog>
        ];
        if (emptyObject(this.state.product_fast_view) != true) {
             productModal = [
                <Dialog
                    ref="productDialog"
                    style={{
                        overflow: 'scroll'
                    }}
                    title="Быстрый просмотр товара"
                    actions={modalActions}>
                    <ProductFastView  product={this.state.product_fast_view}/>
                </Dialog>
                ];
        }
        return (
            <div>
                {productModal}
            </div>
        )
    }
});


module.exports = ProductModal;
