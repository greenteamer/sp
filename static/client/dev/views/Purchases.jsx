var React = require('react');
var Catalogs = require('./Catalogs.jsx');
var PurchasesActions = require('../actions/PurchasesActions.js');


var Purchase = React.createClass({
    render: function () {
        var description = this.props.purchase.description.slice(0,100);
        description = description.replace(/(<([^>]+)>)/ig,"");
        return (
            <div className="purchase-item">
                <div className="row">
                    <div className="col-xs-4 purchase-info">
                        <h2>{this.props.purchase.name}</h2>
                        <p>{description}</p>
                    </div>
                    <div className="col-xs-8 purchase-info">
                        <Catalogs catalogs={this.props.purchase.catalogs} />
                    </div>
                </div>
            </div>
        )
    }
});


var Purchases = React.createClass({
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
        var length = this.props.collection.length;
        var items = this.props.collection.map(function (item, index){
            if (index === length-1) {
                return (
                    <div>
                        <Purchase key={item.id} purchase={item}/>
                    </div>
                )
                }
            else {
                return (
                    <div>
                        <Purchase key={item.id} purchase={item}/>
                        <div className="separator"></div>
                    </div>
                )
            }
        });
        return (
            <div className="purchases-list">
                <h2 className="font-decor block-title">{this.props.title}</h2>
                <div className="block-buttons">
                    <button type="button" className="btn btn-primary" onClick={this.getPopularPromo}>Популярные</button>
                    <button type="button" className="btn btn-primary" onClick={this.getNewPromo}>Новые</button>
                    <button type="button" className="btn btn-primary" onClick={this.getHotPurchases}>Горящие</button>
                </div>
                {items}
            </div>
        )
    }
});


module.exports = Purchases;
