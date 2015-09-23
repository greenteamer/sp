var React = require('react');
var IF = require('../customhelpers/IF.jsx');


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
    			);
        	};
        });
        var link = "/purchases/" + this.props.purchase.id + "/";

        return (
            <div>
                <h2>{this.props.purchase.name}</h2>
                <IF condition={this.props.view_state.view_page == 'purchase'}>
                    <div>                        
                        {status}                
                        <div dangerouslySetInnerHTML={createDescription()} />             
                    </div>
                </IF>
                <IF condition={this.props.view_state.view_page != 'purchase'}>
                    <div>                         
                        <a className="btn btn-primary purchase_link" href={link}>подробнее о закупке</a>
                    </div>
                </IF>
            </div>
        );
        	
	}
});


module.exports = PurchaseDetailInfo;