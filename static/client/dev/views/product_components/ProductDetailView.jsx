var React = require('react');
var PurchasesActions = require('../../actions/PurchasesActions.js');
var PurchasesStore = require('../../stores/PurchasesStore.js');
var ProductDetailForm = require('./ProductDetailForm.jsx');
var PhotoModal = require('./PhotoModal.jsx');
var Benefits = require('../Benefits.jsx');
var Tabs = require('material-ui').Tabs;
var Tab = require('material-ui').Tab;
var ThemeManager = require('material-ui/lib/styles/theme-manager')();
var Colors = require('material-ui').Styles.Colors;

// for FAQ
var FaqStore = require('../../faq/stores/FaqStore.js');
var FaqActions = require('../../faq/actions/FaqActions.js');
var FAQ = require('../../faq/views/App.jsx');

var $ = require('jquery');
var _ = require('underscore');

function emptyObject(obj) {
    //вспомогательная функция проверяет пуст ли объект
    for (var i in obj) {
        return false;
    }
    return true;
}


var ProductFastView = React.createClass({
    childContextTypes: {
        muiTheme: React.PropTypes.object
    },
    getChildContext: function() {
        return {
            muiTheme: ThemeManager.getCurrentTheme()
        };
    },
    getInitialState: function () {
        return {
            purchase: {},
            questions: [],
            user: {},
            organizers: [],
            
            // для проверки может ли user отвечать на комментарии
            is_owner: false,
            
            // для изменения стиля по scroll для формы
            fixed_style: {
                position: 'relative',
                top: '0px'
            }

        };
    },
    componentWillMount: function(){        
        ThemeManager.setPalette({
           accent1Color: Colors.amber400
        });
        FaqActions.getCurrentUser();        
        FaqStore.bind( 'change', this.userChanged );   
        PurchasesStore.bind('organizersTrigger', this.changeOrganizers);
        FaqStore.bind( 'questionsChange', this.questionsChange );      
    },    
    componentWillUnmount: function  () {               
        FaqStore.unbind( 'change', this.userChanged );  
        PurchasesStore.unbind('organizersTrigger', this.changeOrganizers);
        FaqStore.unbind( 'questionsChange', this.questionsChange );
    },
    componentDidMount: function () {
        window.addEventListener('scroll', this.handleScroll);  
    },
    componentDidUnmount: function () {
        window.removeEventListener('scroll', this.handleScroll);    
    },
    handleScroll: function () {
        // изменяем позицию формы по скролу
        var top = $(document).scrollTop();
        var fixed_style = {}; 
        if (top < 750) {
            fixed_style = {
                position: 'relative',
                top: '0px'            
            };
        } else {
            fixed_style = {
                position: 'fixed',
                top: '50px',             
                width: '250px',
                zIndex: 100,
                right: '15px'
            };
        }
        this.setState({
            fixed_style : fixed_style
        });
    },  
    userChanged: function () {
        PurchasesActions.getOrganizers();
        this.setState({
            user: FaqStore.user
        });                 
    },
    changeOrganizers: function () {
        // только когда получили профили делаем get запрос на список вопросов
        FaqActions.getFaqTree();
        // при получении всех профайлов находим профайл текущего пользователя state.user        
        tmp_user = this.state.user;
        // console.log('organizer_profiles: ', PurchasesStore.organizer_profiles); 
        tmp_profile = _.find(PurchasesStore.organizer_profiles, function (profile) {
            // console.log('profile in organizer_profiles: ', profile);    
            return profile.user = tmp_user.id;
        });

        // находим текущую закупку
        var tmp_this_purchase = {};
        var tmp_product = this.props.product;
        _.each(PurchasesStore.categories, function (cat) {
            _.each(cat.category_purchase, function (purch) {
                _.each(purch.catalogs, function (catalog) {
                    if (catalog.id == tmp_product.catalog) {
                        tmp_this_purchase = purch;
                    };
                });
            });
        });    


        // console.log('find profile in PurchasesStore.collection: ', PurchasesStore.collection);
        var check = _.some(tmp_profile.purchases, function (purchase) {
            // проходимя по всем его закупкам (tmp_profile.purchases) и возвращяем true в check если 
            // id текущей закупки хоть однажды совпадет с id одной из его закупок
            return purchase.id == tmp_this_purchase.id;
        });

        // меняем состояние компонента
        // console.log('is_owner: ', check);
        this.setState({
            purchase: tmp_this_purchase,
            organizers: PurchasesStore.organizer_profiles,
            is_owner: check
        });
    },
    questionsChange: function () {
        // console.log('FAQ start questionsChange, FaqStore.questions: ', FaqStore.questions);
        var purchase_id = this.state.purchase.id;
        // console.log('FAQ start questionsChange purchase_id: ', purchase_id);
        var product_id = this.props.product.id;
        var tmp_questions = _.filter(FaqStore.questions, function (question) {
            return (question.purchase == purchase_id && question.product == product_id);
        });
        // console.log('FAQ questionsChange tmp_questions: ', tmp_questions);
        this.setState({
            questions: tmp_questions
        });    
    },
    render: function(){
        // console.log('ProductDetailView start render');
        // console.log('ProductDetailView this.props.product', this.props.product);
        // console.log('ProductDetailView PurchasesStore.categories', PurchasesStore.categories);
        // console.log('ProductDetailView this.state.purchase', this.state.purchase);
        // console.log('ProductDetailView this.state.questions', this.state.questions);
        var description = this.props.product.description;
        description = (description.substr(0, 350));
        var tabsStyle = {
            'tabs': {
                'border': '1px solid #C5C5C5',
                'padding': '15px'},
            'tab': {
                'background': '#443f39'}
            };
        var images = this.props.product.images.map(function (image, count) {
            if (count != 0 && count < 5) {
                return (
                    <div className="product_small_image" style={{paddingRight: '12px'}}>
                        <a className="fancybox" rel="gallery1" href={image.image}>
                            <img style={{marginTop: '10px'}} src={image.cropping_url}/>
                        </a>
                    </div> 
                );
            };
        });

        return (
            <div className="product_view">
                <div className="col-xs-12 col-sm-5 col-md-5 product_fast_view">
                    <div className="row">
                        <div className="col-xs-12">
                            <a className="fancybox" rel="gallery1" href={this.props.product.images[0].image}>
                                <img src={this.props.product.images[0].cropping_url_cart}/>
                            </a>
                        </div>
                        <div className="product_small_image_container">
                            {images}
                        </div>
                    </div>
                </div>
                <div className="col-xs-12 col-sm-7 col-md-7 product_fast_view">
                    <div className="row">
                        <div className="col-xs-12">
                            <div className="row">
                                <div className="col-xs-12 col-sm-8 col-md-9">
                                    <h2>{this.props.product.product_name}</h2>
                                    <p>Артикул: <b>{this.props.product.sku}</b></p>
                                </div>                                
                            </div>
                        </div>                        
                        <div className="col-xs-12 col-sm-12 col-md-12">
                            <div style={this.state.fixed_style}>
                                <ProductDetailForm product={this.props.product} cpp_catalog={this.props.product.cpp_catalog} />
                            </div>
                        </div>
                        <div className="col-xs-12 col-sm-12 col-md-12">
                            <Benefits />
                        </div>
                    </div>
                </div>
                <div className="col-xs-12 col-sm-12 col-md-12">
                    <div className="full-description">
                        <Tabs className="my_tabs" style={tabsStyle.tabs}>
                            <Tab label="Описание" style={tabsStyle.tab}>
                                <div>
                                    <h2>Описание</h2>
                                    <p>
                                        {this.props.product.description}
                                    </p>
                                </div>
                            </Tab>
                            <Tab label="Комментарии" style={tabsStyle.tab}>
                                <div>
                                    <h2>Комментарии</h2>
                                    <FAQ 
                                        questions={this.state.questions}
                                        purchase={this.state.purchase}
                                        product={this.props.product}
                                        user={this.state.user}
                                        is_owner={this.state.is_owner}/>
                                </div>
                            </Tab>
                        </Tabs>
                    </div>
                </div>
                <PhotoModal image={this.props.product.images[0]} />
            </div>
        );

    }
});


module.exports = ProductFastView;
