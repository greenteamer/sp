var React = require('react');
var Slider = require('react-slick');
var ProductForm = require('./ProductForm.jsx');
var PurchasesActions = require('../../actions/PurchasesActions.js');
var PurchasesStore = require('../../stores/PurchasesStore.js');
var Dialog = require('material-ui').Dialog;
var FlatButton = require('material-ui').FlatButton;
var ThemeManager = require('material-ui/lib/styles/theme-manager')();
var ProductTileView = require('./ProductTileView.jsx');
var ProductRelativeTitle = require('./ProductRelativeTitle.jsx');

var IF = require('../customhelpers/IF.jsx');


var ProductInfoMini = React.createClass({
    childContextTypes: {
        muiTheme: React.PropTypes.object
    },
    getChildContext: function() {
        return {
            muiTheme: ThemeManager.getCurrentTheme()
        };
    },
    showProduct: function(){
        var data = {
            item: this.props.item,
            purchase_id: this.props.purchase_id,
            cpp_catalog: this.props.cpp_catalog
        };
        PurchasesActions.fastShowProduct(data);
    },
    render: function(){
        var link = "/products/" + this.props.item.id + "/";
        return (
            <div>
                <div className="image-wrapper">
                    <img src={this.props.item.images[0].image}/>
                    <div className="blackout"></div>
                    <button type="button" className="btn btn-primary fast-modal bottom" onClick={this.showProduct}>
                        <i className="mdi-content-content-copy"></i>
                    </button>
                    <a href={link} className="btn btn-primary fast-modal top">
                        <i className="mdi-action-search"></i>
                    </a>
                </div>
                <h5 className="product_name_mini">{this.props.item.product_name}</h5>
                <p className="price">{this.props.item.price}</p>
            </div>
        )
    }
});


var SimpleSlider = React.createClass({
    getInitialState: function () {
        return {
            view_state: PurchasesStore.view_state
        }  
    },
    componentWillMount: function () {
        PurchasesStore.bind('changeViewState', this.setViewState);
    },
    componentWillUnmount: function () {
        PurchasesStore.unbind('changeViewState', this.setViewState);
    },
    setViewState: function () {
        this.setState({
            view_state: PurchasesStore.view_state
        });
    },
    render: function () {
        var settings = {
            dots: true,
            arrows: true,
            infinite: true,
            speed: 500,
            slidesToShow: 3,
            slidesToScroll: 4
        };
        var cpp_catalog = this.props.cpp_catalog;
        var purchase_id = this.props.purchase_id;
        var tmp_view_state = this.state.view_state.view_page;
        var items = this.props.items.map(function(item){
            text = item.description.slice(0,100);

            return (
                <div key={item.id}>                    
                    <IF condition={tmp_view_state != 'category'}>
                        <ProductTileView key={item.id} product={item}/>
                    </IF>
                    <IF condition={tmp_view_state == 'category'}>
                        <ProductRelativeTitle key={item.id} product={item}/>
                    </IF>
                </div>
            )            
            // return (
            //     <div key={item.id}>
            //         <ProductInfoMini item={item} purchase_id={purchase_id} cpp_catalog={cpp_catalog}/>
            //         <ProductForm key={item.id} product={item} cpp_catalog={cpp_catalog}/>
            //     </div>
            // )
        });
        return (
          <Slider {...settings}>
              {items}
          </Slider>
        );
    }
});


module.exports = SimpleSlider;
