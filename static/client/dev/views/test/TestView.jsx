var React = require('react');
var $ = require('jquery');


var Product = React.createClass({
	render: function(){
		return (
			<div>
				<h2>{this.props.name}</h2>
				<p>{this.props.description}</p>
				<p>{this.props.price}</p>
			</div>
		)
	}
});


var TestView = React.createClass({
	getInitalState: function(){
		return {
			name: "",
			description: "",
			price: 0
		}
	},
	componentWillMount: function(){
		this.setState({
			name: "name",
			description: "description",
			price: 1
		});
	},
	changeName: function(e){
		this.setState({
			name: e.target.value
		});
	},
	render: function () {
		return (
            <div>
				<Product
					name={this.state.name}
					description={this.state.description}
					price={this.state.price} />
				<input type="text" value={this.state.name} onChange={this.changeName} />
            </div>
		)
	}
});


module.exports = TestView;
