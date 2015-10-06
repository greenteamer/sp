React = require('react')
$ = require('jquery')
Purchases = require('./Purchases.jsx')
PurchasesStore = require('../stores/PurchasesStore.js')
PromoFilter = require('./PromoFilter.jsx')
PurchasesActions = require('../actions/PurchasesActions.js')


PopularIndex = React.createClass

  getInitialState: ->
    collection: []
    user: {}
    title: ''

  componentDidMount: ->
    PurchasesActions.getPopularPromo()
    PurchasesStore.bind('change', this.collectionChanged)

  componentWillUnmount: ->
    PurchasesStore.unbind('change', this.collectionChanged)

  collectionChanged: ->
    @setState
      collection: PurchasesStore.collection

  render: ->
    collection = []
    title = ''
    @state.collection.forEach (item) ->
      collection = item.promo_purchase
      title = item.name

    <div>
      <h2 className="font-decor block-title">{title}</h2>
      <PromoFilter />
      <Purchases
        collection={collection}
        title={title}
        indicatorElementName='#popular'/>
    </div>


module.exports = PopularIndex
