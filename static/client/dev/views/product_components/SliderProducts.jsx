var React = require('react');
var Slider = require('react-slick');
var ProductForm = require('./ProductForm.jsx');


var SimpleSlider = React.createClass({
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
            <div key={item.id}>
                <div className="image-wrapper">
                    <img src={item.images[0].image}/>
                    <div className="blackout"></div>
                </div>
                <h5 className="product_name_mini">{item.product_name}</h5>
                <p className="price">{item.price}</p>
                <ProductForm key={item.id} product={item} cpp_catalog={cpp_catalog}/>
            </div>
        )
    });
    return (
      <Slider {...settings}>
          {items}
      </Slider>
    );
  }
});


module.exports = SimpleSlider;
