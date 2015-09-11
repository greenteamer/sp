var React = require('react');
var PurchasesActions = require('../../actions/PurchasesActions.js');
var PurchasesStore = require('../../stores/PurchasesStore.js');
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

var PhotoModal = React.createClass({
    getInitialState: function () {
        return {
            image: PurchasesStore.modal_photo
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
    componentWillMount: function () {
        PurchasesStore.bind('photoView', this.showPhoto);  
    },
    componentWillUnmount: function () {
        PurchasesStore.unbind('photoView', this.showPhoto);  
    },
    showPhoto: function () {
        this.setState({
            image: PurchasesStore.modal_photo
        });  
        this.refs.photoModal.show();
    },
    _DialogCancel: function () {
    	this.refs.photoModal.dismiss();
    },
    render: function(){
        console.log('PhotoModal render this.state.image: ', this.state.image);
        var modalActions = [
			  <FlatButton
			    label="Закрыть"
			    secondary={true}
			    className="modal-button-cancel btn btn-default"
			    onClick={this._DialogCancel} />
        ];
        var photoModal = [
            <Dialog
                ref="photoModal"
                className="test_modal"
                title="Фото"
                style={{
                    overflow: 'scroll',
                    zIndex: 1000                    
                }}      
                actions={modalActions}>
                <img style={{width: "100%"}} src={this.state.image.image} />
            </Dialog>
        ];        
        return (
            <div>
                {photoModal}
            </div>
        )
    }
});


module.exports = PhotoModal;