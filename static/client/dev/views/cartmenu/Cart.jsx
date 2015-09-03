var React = require('react');
var Store = require('../../stores/PurchasesStore.js');
var Actions = require('../../actions/PurchasesActions.js');


var Cart = React.createClass({
	render: function  () {
		return (
			<div>
				<h2 className="font-decor block-title">Корзина</h2>
			</div>
		)
	}
});


module.exports = Cart;