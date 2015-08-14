var Catalogs = require('./Catalogs.jsx');
var PurchasesActions = require('../actions/PurchasesActions.js');


var Purchase = React.createClass({displayName: "Purchase",
    render: function () {
        var description = this.props.purchase.description.slice(0,100);
        return (

            React.createElement("div", {className: "panel panel-default"}, 
                React.createElement("div", {className: "panel-body"}, 
                    React.createElement("div", {className: "purchase-item"}, 
                        React.createElement("div", {className: "row"}, 
                            React.createElement("div", {className: "col-xs-4 purchase-info"}, 
                                React.createElement("h2", null, this.props.purchase.name), 
                                React.createElement("p", null, description)
                            ), 
                            React.createElement("div", {className: "col-xs-8 purchase-info"}, 
                                React.createElement(Catalogs, {catalogs: this.props.purchase.catalogs})
                            )
                        )
                    )
                )
            )
        )
    }
});


var Purchases = React.createClass({displayName: "Purchases",
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
        items = this.props.collection.map(function (item){
            return (
                React.createElement(Purchase, {key: item.id, purchase: item})
            )
        });
        var title = 'Горящие';
        return (
            React.createElement("div", {className: "purchases-list"}, 
                React.createElement("h2", {className: "font-decor block-title"}, this.props.title), 
                React.createElement("div", {className: "block-buttons"}, 
                    React.createElement("button", {type: "button", className: "btn btn-primary", onClick: this.getPopularPromo}, "Популярные"), 
                    React.createElement("button", {type: "button", className: "btn btn-primary", onClick: this.getNewPromo}, "Новые"), 
                    React.createElement("button", {type: "button", className: "btn btn-primary", onClick: this.getHotPurchases}, "Горящие")
                ), 
                items
            )
        )
    }
});


module.exports = Purchases;