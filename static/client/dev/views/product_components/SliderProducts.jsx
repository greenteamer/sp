var React = require('react');
var Slider = require('react-slick');
var ProductForm = require('./ProductForm.jsx');
var PurchasesActions = require('../../actions/PurchasesActions.js');
var PurchasesStore = require('../../stores/PurchasesStore.js');
var Dialog = require('material-ui').Dialog;
var FlatButton = require('material-ui').FlatButton;
var ThemeManager = require('material-ui/lib/styles/theme-manager')();
var ProductHoverTitle = require('./ProductHoverTitle.jsx');
var ProductRelativeTitle = require('./ProductRelativeTitle.jsx');

var IF = require('../customhelpers/IF.jsx');


var SimpleSlider = React.createClass({
    render: function () {
        if (this.props.view_state.view_page == 'purchase') {
            // колличество слайдов больше на странице закупки 
            var settings = {
                dots: true,
                arrows: true,
                infinite: true,
                speed: 500,
                slidesToShow: 4,
                slidesToScroll: 5
            };
        } else {
            var settings = {
                dots: true,
                arrows: true,
                infinite: true,
                speed: 500,
                slidesToShow: 3,
                slidesToScroll: 4
            };
        }        
        var cpp_catalog = this.props.cpp_catalog;
        var purchase_id = this.props.purchase_id;
        var tmp_view_state = this.props.view_state;
        var items = this.props.items.map(function(item){
            text = item.description.slice(0,100);
            return (
                <div key={item.id}>                    
                    <IF condition={tmp_view_state.view_page != 'category'}>
                        <ProductHoverTitle 
                            key={item.id} 
                            product={item}
                            view_state={tmp_view_state}/>
                    </IF>
                    <IF condition={tmp_view_state.view_page == 'category'}>
                        <ProductRelativeTitle 
                            key={item.id} 
                            product={item}
                            view_state={tmp_view_state}/>
                    </IF>
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
