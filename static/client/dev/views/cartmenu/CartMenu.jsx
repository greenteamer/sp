var React = require('react');
var $ = require('jquery');
var Purchases = require('../Purchases.jsx');
var PurchasesStore = require('../../stores/PurchasesStore.js');
var PurchasesActions = require('../../actions/PurchasesActions.js');


var CartItem = React.createClass({
    render: function(){
        //<h3>{this.props.item.name}</h3>
        //        <ul>
        //            {properties}
        //        </ul>
        //        <p>{this.props.item.price}</p>
        //        <p>{this.props.item.quantity}</p>
        var property_values = this.props.item.properties.split(',');
        var properties = property_values.map(function(property){
            return(
                <li>{property}</li>
            )
        });
        return (
            <div>
                <div className="small-banner">
                    <img src={this.props.item.image} alt="" className="cart-image" />
                    <div className="info">
                        <div className="inner">
                            <p className="p1">{this.props.item.name}</p>
                            <p className="p2">{properties}</p>
                            <p className="p2">{this.props.item.price} р.</p>
                            <span className="quantity">{this.props.item.quantity}</span>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
});


var CartMenu = React.createClass({
	getInitialState: function () {
        return {
            cartitems: []
        }
    },
    componentWillMount: function(){
        PurchasesActions.getCartItems();
    },
    componentDidMount: function () {
        //обновляем store в соответствии с текущей категорией
        //PurchasesActions.getCartItems();
        PurchasesStore.bind( 'change', this.collectionChanged );
    },
    componentWillUnmount: function () {
        PurchasesStore.unbind( 'change', this.collectionChanged );
    },
    collectionChanged: function () {
		this.setState({
            cartitems: PurchasesStore.cartitems
        });
    },
	render: function () {
        var items = this.state.cartitems.map(function (item) {
            return (
                <CartItem item={item} />
            )
        });
		return (
            <li className="dropdown">
                <a href="" data-target="#" className="dropdown-toggle" data-toggle="dropdown">Корзина <b className="caret"></b></a>
                <ul className="dropdown-menu">
                    <div className="cart_button_wrapper">
                        <a href="/cart/" className="btn btn-primary full-width">перейти в корзину</a>
                    </div>
                    {items}
                </ul>
            </li>
		)
	}
});


module.exports = CartMenu;
