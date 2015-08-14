var $ = require('jquery');
var Purchases = require('./Purchases.jsx');
var PurchasesStore = require('../stores/PurchasesStore.js');

// actions
var PurchasesActions = require('../actions/PurchasesActions.js');


var App = React.createClass({displayName: "App",
	getInitialState: function () {
        return {
            collection: [],
          	user: {}
        }
    },
    componentDidMount: function () {
		PurchasesActions.getAllPromo();
        PurchasesStore.bind( 'change', this.collectionChanged );
        console.log('component did mount');
    },
    componentWillUnmount: function () {
        console.log('component will unmount');
        PurchasesStore.unbind( 'change', this.collectionChanged );
    },
    collectionChanged: function () {
		this.setState({
            collection: PurchasesStore.collection
        });
    },
	render: function () {
		return (
            React.createElement("div", null, 
		         React.createElement(Purchases, {collection: this.state.collection})
            )
		)
	}
});

module.exports = App;