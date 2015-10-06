React = require('react')
PopularIndex = require('../views/PopularIndex.cjsx')
injectTapEventPlugin = require("react-tap-event-plugin")

injectTapEventPlugin 

React.render <PopularIndex />, document.getElementById 'popular'
