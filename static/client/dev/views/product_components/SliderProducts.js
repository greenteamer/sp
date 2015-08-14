var Slider = require('react-slick');
var ProductForm = require('./ProductForm.jsx');


var SimpleSlider = React.createClass({displayName: "SimpleSlider",
  render: function () {
    var settings = {
      dots: true,
      infinite: true,
      speed: 500,
      slidesToShow: 3,
      slidesToScroll: 4
    };
    var cpp_catalog = this.props.cpp_catalog;
    var items = this.props.items.map(function(item){
        text = item.description.slice(0,100);
        return (
            React.createElement("div", {key: item.id}, 
                React.createElement("div", {className: "image-wrapper"}, 
                    React.createElement("img", {src: item.images[0].image}), 
                    React.createElement("div", {className: "blackout"})
                ), 
                React.createElement("h5", {className: "product_name_mini"}, item.product_name), 
                React.createElement("p", {className: "price"}, item.price), 
                React.createElement(ProductForm, {key: item.id, product: item, cpp_catalog: cpp_catalog})
            )
        )
    });
    return (
      React.createElement(Slider, React.__spread({},  settings), 
          items
      )
    );
  }
});


module.exports = SimpleSlider;