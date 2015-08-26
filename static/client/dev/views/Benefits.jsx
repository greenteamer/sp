var React = require('react');
var PurchasesActions = require('../actions/PurchasesActions.js');
var PurchasesStore = require('../stores/PurchasesStore.js');


var Benefits = React.createClass({
    getInitialState: function(){
        return {
            benefits: [],
            select_benefit: {}
        }
    },
    componentWillMount: function(){
        PurchasesActions.getBenefits();
        PurchasesStore.bind('changeBenefits', this.changeBenefits);
    },
    changeBenefits: function(){
        this.setState({
            benefits: PurchasesStore.benefits,
            select_benefit: PurchasesStore.benefits[0]
        });
    },
    changeSelect: function(){
        console.log('click');
        this.setState({
            benefits: PurchasesStore.benefits,
            select_benefit: PurchasesStore.benefits[1]
        });
    },
    render: function () {
        var benefits = this.state.benefits.map(function(benefit){
            benefit.description = benefit.description.replace(/(<([^>]+)>)/ig,"");
            return (
                <div className="col-xs-12 col-sm-6 col-md-4">
                    <a name="" >{benefit.name}</a>
                </div>
            )
        });
        return (
            <div className="benefits">
                <div className="row">
                    <div className="col-xs-12">
                        <div className="benefits-header">
                            <div className="row">
                                {benefits}
                            </div>
                        </div>
                    </div>
                    <div className="col-xs-12">
                        <div className="benefits-separator">
                            <h3>{this.state.select_benefit.name}</h3>
                        </div>
                    </div>
                    <div className="col-xs-12">
                        <div className="benefits-content">
                            {this.state.select_benefit.description}
                        </div>
                    </div>
                </div>
            </div>
        )
    }
});


module.exports = Benefits;
