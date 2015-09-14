var React = require('react');


var Answer = React.createClass({
	render: function () {
		return (
			<div className="list-group-item">
				<div className="row-picture">
					<img className="circle" src={this.props.photo} />
        		</div>
        		<div className="row-content">
        			<h4 className="list-group-item-heading">{this.props.name} <span className="small">{this.props.date}</span></h4>
        			<p className="list-group-item-text">{this.props.text}</p>
				</div>
			</div>
		)
	}
});


var AnswerList = React.createClass({
	render: function (){
		answers = this.props.answers.map(function (answer) {
			return (
				<div>
					<Answer name={answer.name} text={answer.text} photo={answer.photo} date={answer.date} />				
					<div className="list-group-separator"></div>
				</div>
			)
		});
		return (
			<div className="list-group">	
				{answers}
			</div>
		)
	}
});


module.exports = AnswerList;