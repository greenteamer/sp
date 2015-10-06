React = require('react')
$ = require('jquery')
_ = require('underscore')
Catalogs = require('./Catalogs.jsx')
PurchasesActions = require('../actions/PurchasesActions.js')
PurchasesStore = require('../stores/PurchasesStore.js')
ButtonsView = require('./ButtonsView.jsx')
ProductModal = require('./product_components/ProductModal.jsx')
ProductHoverTitle = require('./product_components/ProductHoverTitle.jsx')
ProductRelativeTitle = require('./product_components/ProductRelativeTitle.jsx')
PurchaseDetailInfo = require('./purchase/PurchaseDetailInfo.jsx')
FaqActions = require('../faq/actions/FaqActions.js')

#material-ui
mui = require('material-ui')
IconButton = mui.IconButton
ThemeManager = require('material-ui/lib/styles/theme-manager')()

#my custom helpers
IF = require('./customhelpers/IF.jsx')
MyRefreshIndicator = require('./customhelpers/MyRefreshIndicator.jsx')
Methods = require('./customhelpers/Methods.coffee')


CatalogTileView = React.createClass(
  render: ->
    # Устанавливаем классы для каждого товара в зависимости от view_state.view_page
    # Получаем view_state из PurchaseTileView
    products_class = ''
    if @props.view_state.view_page == 'purchase'
      products_class = 'col-xs-12 col-sm-4 col-md-3'
    else
      products_class = 'col-xs-12 col-sm-6 col-md-4'
    tmp_cpp = @props.catalog.cpp_catalog
    tmp_view_state = @props.view_state
    items = @props.catalog.product_catalog.map((product) ->
      product.cpp_catalog = tmp_cpp
      return
        <div className={products_class}>
            <IF condition={tmp_view_state.view_page != 'category'}>
                <ProductHoverTitle product={product}/>
            </IF>
            <IF condition={tmp_view_state.view_page == 'category'}>
                <ProductRelativeTitle product={product}/>
            </IF>
        </div>
    )
    return
      <div className="row">
          <div className="col-xs-12">
              <h5>Каталог: {this.props.catalog.catalog_name}</h5>
          </div>
          {items}
      </div>
)


PurchaseTileView = React.createClass(
  render: ->
    # Устанавливаем классы для каждой закупки в зависимости от view_state.view_page
    # Получаем view_state из Purchases
    info_class = ''
    products_class = ''
    if @.props.view_state.view_page == 'purchase'
      info_class = "col-xs-12 col-md-12"
      products_class = "col-xs-12 col-md-12"
    else
      info_class = "col-xs-12 col-md-4"
      products_class = "col-xs-12 col-md-8"

    tmp_view_state = @.props.view_state
    items = @.props.purchase.catalogs.map((catalog) ->
      return
        <CatalogTileView
          catalog={catalog}
          view_state={tmp_view_state}/>
    )

    var link = "/purchases/" + this.props.purchase.id + "/";
    return (
        <div className="purchase_tile_view">
            <div className="row">
                <div className={info_class}>
                    <div className="purchase_tile_title">
                        <IF condition={this.props.view_state.view_page == 'purchase'}>
                            <PurchaseDetailInfo
                                purchase={this.props.purchase}
                                view_state={this.props.view_state}/>
                        </IF>
                        <IF condition={this.props.view_state.view_page != 'purchase'}>
                            <div>
                                <h2 className="tile_view">{this.props.purchase.name}</h2>
                                <a className="btn btn-primary purchase_link" href={link}>подробнее о закупке</a>
                            </div>
                        </IF>
                    </div>
                </div>
                <div className={products_class}>
                    {items}
                </div>
            </div>
        </div>
    );

)
