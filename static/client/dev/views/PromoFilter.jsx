var React = require('react');
var Catalogs = require('./Catalogs.jsx');
var PurchasesActions = require('../actions/PurchasesActions.js');


var PromoFilter = React.createClass({
    getPopularPromo: function(e){
        e.preventDefault();
        PurchasesActions.getPopularPromo();
    },
    getNewPromo: function(e){
        e.preventDefault();
        PurchasesActions.getNewPromo();
    },
    getHotPurchases: function(e){
        e.preventDefault();
        PurchasesActions.getHotPurchases();
    },
    render: function () {
        return (
            <div className="block-buttons">
                <button type="button" className="btn btn-primary" onClick={this.getPopularPromo}>Популярные</button>
                <button type="button" className="btn btn-primary" onClick={this.getNewPromo}>Новые</button>
                <button type="button" className="btn btn-primary" onClick={this.getHotPurchases}>Горящие</button>
            </div>
        )
    }
});


module.exports = PromoFilter;