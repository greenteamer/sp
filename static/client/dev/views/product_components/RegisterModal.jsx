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
            message: {}
        }
    },
    componentWillMount: function () {
        PurchasesStore.bind('messageView', this._DialogShow);
    },
    componentWillUnmount: function () {
        PurchasesStore.unbind('messageView', this._DialogShow);
    },
    _DialogShow: function (){
        this.setState({
            message: PurchasesStore.message_modal
        });
        this.refs.registerDialog.show();
    },
    _DialogCancel: function () {
    	this.refs.registerDialog.dismiss();
    },
    render: function(){
        if (this.props.is_show == true){
            this._DialogShow();
        }
        console.log('RegisterModal is_show: ', this.props.is_show);
        var modalActions = [
			  <FlatButton
			    label="Закрыть"
			    secondary={true}
			    className="modal-button-cancel btn btn-default"
			    onClick={this._DialogCancel} />
        ];
        var productModal = [
            <Dialog
                ref="registerDialog"
                title="Быстрый просмотр товара"
                actions={modalActions}>
                <p>{this.state.message.text}</p>
                <p><a href={this.state.message.link}>подробнее</a></p>
            </Dialog>
        ];
        return (
            <div>
                {productModal}
            </div>            
        );
    }
});


module.exports = ProductModal;
