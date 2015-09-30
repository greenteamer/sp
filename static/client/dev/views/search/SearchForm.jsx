var React = require('react');
// var PurchasesActions = require('../../actions/PurchasesActions.js');
var SearchStore = require('../../stores/SearchStore.js');
var SearchActions = require('../../actions/SearchActions.js');


var Search = React.createClass({
    searchFunc: function(e){
        var query = React.findDOMNode(this.refs.query_text).value;
        SearchActions.changeSearchState(query);
        e.preventDefault();
    },
	render: function () {
		return (            
            <div className="custom-form">
                <input type="text" ref="query_text" className="col-lg-8" placeholder="поиск товаров"/>
                <button onClick={this.searchFunc} type="submit" className="btn btn-primary pull-left btn-search">
                    <i className="mdi-action-search"></i>
                </button>
            </div>            
		);
	}
});


module.exports = Search;
