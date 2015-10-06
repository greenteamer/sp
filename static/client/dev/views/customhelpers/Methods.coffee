# -- * -- CHACKPROPERTIES -- * --
# chackProperties - проверка существования комбинации свойств в товаре
# принимает 2 обязательных параметра:
# cpp_properties - массив свойств, который находится в состоянии компонента формы (включает в себя обязательный параметр value - который лежит в объекте каждого свойства, которое заполняет пользователь)
# product_properties - строка в которой через ";" перечислены все возможные комбинации свойств данного товара
# функция chackProperties проверяет все ли параметры заполнил пользователь, создает из их значений строку в которой они перечислены через "," и проверяет эту строку на совпадение среди всех возможных вариантов
# -- * --

_ = require 'underscore'
$ = require 'jquery'
snakbar = require '../../../lib/snackbar.js'


Methods =
  convertCategoriesToFlatProducts: (collection) ->
    tmp_collection = []
    collection.forEach (purchase) ->
      purchase.catalogs.forEach (catalog) ->
        catalog.product_catalog.forEach (product) ->
          product.cpp_catalog = catalog.cpp_catalog
          tmp_collection.push product

    tmp_collection

  getAllNestedCategories: (data, category_slug) ->
    # ПОДГОТОВКА КОЛЛЕКЦИИ ВСЕХ ВЛОЖЕННЫХ КАТЕГОРИЙ
    # ***
    # ВАЖНО: работает только с вложенностью не более 3 уровней
    # ***
    # data - коллекция всех категорий категорий
    # category_slug - слаг категории относительно которой мы работаем
    all_categories = []
    if category_slug != undefined && category_slug != ''
      # находим категорию на которую перешел пользователь
      category = _.find(data, (category) -> category.slug == category_slug)
      # Фильтруем все дочерние категории основной
      all_categories = _.filter(data, (cat) -> cat.parent == category.id)
      # проходимся по всем дочерним категориям
      # каждую итерацию фильтруем все категории по parent признаку
      # получаем всех предков изначальной категории
      all_categories_deep = _.map(all_categories, (first_level_cat) ->
        _.filter(data, (cat) -> cat.parent == first_level_cat.id)
      )
      # приводим массив к элементарному виду что бы избежать [ [a], [[b]]]
      all_categories_deep = _.flatten(all_categories_deep, true)
      # объединяем полученные результаты по подкатегориям и по подподкатегориям
      _.union(all_categories, all_categories_deep)
    else
      # если slug = undefined или '' то возвращаем весь массив
      data

  getPurchasesFromCategories: (data, category_slug) ->
    # ПОДГОТОВКА КОЛЛЕКЦИИ ЗАКУПОК КАТЕГОРИИ
    # data - строковая переменная "slug" категории
    # находим категорию на которую перешел пользователь
    category = _.find(data, (category) -> category.slug == category_slug)
    # получаем все вложенные категории
    all_categories = @.getAllNestedCategories(data, category_slug)
    # добавляем в массив родительскую категорию
    all_categories.unshift(category)
    # создаем массив из всех значений поля "category_purchase"
    all_purchases_arr = _.pluck(all_categories, "category_purchase")
    # приводим к элементарному виду и возвращяем
    _.flatten(all_purchases_arr, true)

  getCatalogsFromCategories: (initial_categories, category_slug) ->
    # находим категорию на которую перешел пользователь
    category = _.find(initial_categories, (category) -> category.slug == category_slug)
    # получаем все вложенные категории
    all_categories = @.getAllNestedCategories(initial_categories, category_slug)
    # добавляем в массив родительскую категорию
    all_categories.unshift(category)
    # получаем id всех категорий включая вложенные
    category_id_arr = _.pluck(all_categories, 'id')
    # ПОЛУЧАЕМ ВСЕ КАТАЛОГИ
    # создаем массив из всех значений поля "category_purchase"
    all_purchases_arr = _.pluck(initial_categories, "category_purchase")
    # приводим к элементарному виду
    all_purchases = _.flatten(all_purchases_arr, true)
    all_catalogs_arr = _.pluck(all_purchases, "catalogs")
    # приводим к элементарному виду
    all_catalogs = _.flatten(all_catalogs_arr, true)
    # ФИЛЬТРУЕМ СОГЛАСНО category_id_arr
    result = _.map(category_id_arr, (id) ->
      # генерируем массив каталогов
      _.filter(all_catalogs, (catalog) ->
        # получаем каталог если хоть один id его категрии совпадает
        _.some(catalog.categories, (category_id) -> category_id == id)
      )
    )
    @unique(_.flatten(result, true))

  convertCatalogsToFlatProducts: (catalogs) ->
    # console.log('Methods convertCatalogsToFlatProducts catalogs: ', catalogs)
    # делаем из массива каталогов массив продуктов
    new_products_arr = _.pluck(catalogs, 'product_catalog')
    _.flatten(new_products_arr, true)

  convertPurchasesToFlatProducts: (collection) ->
    tmp_collection = []
    if collection.length > 0
      collection.forEach (purchase) ->
        purchase.catalogs.forEach (catalog) ->
          catalog.product_catalog.forEach (product) ->
            product.cpp_catalog = catalog.cpp_catalog
            tmp_collection.push(product)
    tmp_collection

  unique: (arr) ->
    # ВОЗВРАЩАЕТ МАССИВ УНИКАЛЬНЫХ ЭЛЛЕМЕНТОВ массива arr
    # обязательное условие: у объектов массива должен быть атрибут id
    # console.log('Methods.unique start , arr: ', arr)
    arr_id = _.uniq(_.pluck(arr, 'id'))  # вернет массив уникальных id -шников массива arr
    # console.log('Methods.unique unoque id arr: ', arr_id)
    _.map(arr_id, (id) ->
      # возвращаем первый эллемент массива arr,
      # id которого есть в массиве уникальных id -шников
      _.find(arr, (el) -> el.id == id)
    )

  unionProductCollections: (collection1, collection2) ->
    # функция объединения 2 коллекций продуктов
    # если первая коллекция пуста - пишем в консоле лог
    c1 = _.pluck(collection1, 'id')  # создаем массив id -шников 1 коллекции
    c2 = _.pluck(collection2, 'id')  # создаем массив id -шников 2 коллекции
    index_arr = _.intersection(c1, c2)  # объединяем уникальные id -шники в один массив
    union = _.union(collection1, collection2)  # объединяем оба массива с прдуктами
    _.map(index_arr, (id) ->
      # возвращаем первый эллемент массива union,
      # id которого есть в массиве уникальных id -шников
      _.find(union, -> (prod) prod.id == id)
    )

  chackProperties: (cpp_properties, product_properties) ->
    # РЕАЛИЗАЦИЯ ПРОВЕРКИ СУЩЕСТВОВАНИЯ КОМБИНАЦИИ СВОЙСТВ
    # проверяем все ли свойства заполнены
    # _.every - возвращает true если все итерации функции вернули true
    properties_filled = _.every(cpp_properties, (property) -> property.value != undefined)

    if properties_filled
      values_str = _.pluck(cpp_properties, 'value').join(',')
      # _.pluck - возвращает массив состоящий из значений полей 'value' объектов массива
      # join - создает из массива выбранных параметров строку параметров через ','
      if _.contains(product_properties.split(''), values_str)
        # _.contains - возвращает true если массив содежит элемент values_str
        $.snackbar
          timeout: 5000
          content: 'Товары с данными характеристиками найдены'
        true
      else
        # выводим сообщение и возвращяем false
        $.snackbar
          timeout: 5000
          content: 'Нет товара с такими характеристиками, пожалуйста, попробуйте другие варианты'
        false

  getCategorySlug: ->
    # получение slug категории по текущему url
    url = $(location).attr('pathname')
    parse_url = url.split('/')[1]
    current_category_slug = parse_url.slice(9)

    if url.split('/')[1] == 'purchases'
      current_category_slug = 'purchase'
    current_category_slug

  getPurchaseIdByUrl: ->
    # получение категорий к которым привязаны каталоги закупки
    url = $(location).attr('pathname')
    url.split('/')[2]


module.exports = Methods
