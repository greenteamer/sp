React = require('react')


App = React.createClass
	render: ->
		(<div>Hello!!!</div>)


React.render <App/>, document.getElementById 'popular'