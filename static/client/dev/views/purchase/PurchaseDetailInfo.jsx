var React = require('react');


var PurchaseDetailInfo = React.createClass({
	render: function  () {               
		var description = this.props.purchase.description;
        function createDescription() { 
            return {__html: description }; 
        };
        var status = this.props.purchase.purchase_status.map(function (status) {
        	if (status.active) {
        		return (
        			<div>
        				<h5>Статус закупки: {status.status.status_name}</h5>
        			</div>
    			)
        	};
        });

        return (
            <div>
                <h2>{this.props.purchase.name}</h2>
                {status}                
                <div dangerouslySetInnerHTML={createDescription()} />             
            </div>
        )
        	
	}
});


module.exports = PurchaseDetailInfo;