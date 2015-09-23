var React = require('react');
//var Category = require('../views/PopularIndex.jsx');
var CartMenu = require('../views/cartmenu/CartMenu.jsx');
var SearchForm = require('../views/search/SearchForm.jsx');
var SearchResult = require('../views/search/SearchResult.jsx');
var Product = require('../views/product/Product.jsx');
var Breadcrumbs = require('../views/breadcrumbs/Breadcrumbs.jsx');
var injectTapEventPlugin = require("react-tap-event-plugin");
var Lightbox = require('react-lightbox');


injectTapEventPlugin();


React.render(
	<Product />,
	document.getElementById('product')
);

React.render(
	React.createElement(Breadcrumbs, null),
	document.getElementById('breadcrumbs')
);

React.render(
	React.createElement(CartMenu, null),
	document.getElementById('cartmenu')
);


React.render(
	React.createElement(SearchForm, null),
	document.getElementById('react_search')
);


React.render(
	React.createElement(SearchResult, null),
	document.getElementById('react_search_result')
);

var Controls = React.createClass({
  render: function () {
    return DOM.div({
      className: 'my-controls'
    }, 
      DOM.div({
        className: 'my-button my-button-left',
        onClick: this.props.backward
      }, '<'),
      DOM.div({
        className: 'my-button my-button-right',
        onClick: this.props.forward
      }, '>')
    );
  }
});

React.render(
  <Lightbox
    pictures={[
      'https://pbs.twimg.com/profile_images/269279233/llama270977_smiling_llama_400x400.jpg',
      'https://pbs.twimg.com/profile_images/1905729715/llamas_1_.jpg',
      'http://static.comicvine.com/uploads/original/12/129924/3502918-llama.jpg',
      'http://fordlog.com/wp-content/uploads/2010/11/llama-smile.jpg'
    ]}
    keyboard
    controls={Controls}
  />
, document.body);

