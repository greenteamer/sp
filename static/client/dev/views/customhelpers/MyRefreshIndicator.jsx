var React = require('react');
//material-ui
var mui = require('material-ui');
var ThemeManager = require('material-ui/lib/styles/theme-manager')();
var RefreshIndicator = mui.RefreshIndicator;


var MyRefreshIndicator = React.createClass({
    childContextTypes: {
        muiTheme: React.PropTypes.object
    },
    getChildContext: function() {
        return {
            muiTheme: ThemeManager.getCurrentTheme()
        };
    },    
    render: function () {
        // relative_element_name - название эллемента , относительно которого
        // будет расчитвываться позиция индикатора
        var indicator_left = $(this.props.relative_element_name).width()/2;
        return (
            <RefreshIndicator size={40} left={indicator_left} top={130} status="loading" />
        )

    }
});


module.exports = MyRefreshIndicator;
