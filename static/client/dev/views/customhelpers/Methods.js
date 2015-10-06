var $, Methods, _, snakbar;

_ = require('underscore');

$ = require('jquery');

snakbar = require('../../../lib/snackbar.js');

Methods = {
  convertCategoriesToFlatProducts: function(collection) {
    var tmp_collection;
    tmp_collection = [];
    collection.forEach(function(purchase) {
      return purchase.catalogs.forEach(function(catalog) {
        return catalog.product_catalog.forEach(function(product) {
          product.cpp_catalog = catalog.cpp_catalog;
          return tmp_collection.push(product);
        });
      });
    });
    return tmp_collection;
  },
  getAllNestedCategories: function(data, category_slug) {
    var all_categories, all_categories_deep, category;
    all_categories = [];
    if (category_slug !== void 0 && category_slug !== '') {
      category = _.find(data, function(category) {
        return category.slug === category_slug;
      });
      all_categories = _.filter(data, function(cat) {
        return cat.parent === category.id;
      });
      all_categories_deep = _.map(all_categories, function(first_level_cat) {
        return _.filter(data, function(cat) {
          return cat.parent === first_level_cat.id;
        });
      });
      all_categories_deep = _.flatten(all_categories_deep, true);
      return _.union(all_categories, all_categories_deep);
    } else {
      return data;
    }
  },
  getPurchasesFromCategories: function(data, category_slug) {
    var all_categories, all_purchases_arr, category;
    category = _.find(data, function(category) {
      return category.slug === category_slug;
    });
    all_categories = this.getAllNestedCategories(data, category_slug);
    all_categories.unshift(category);
    all_purchases_arr = _.pluck(all_categories, "category_purchase");
    return _.flatten(all_purchases_arr, true);
  },
  getCatalogsFromCategories: function(initial_categories, category_slug) {
    var all_catalogs, all_catalogs_arr, all_categories, all_purchases, all_purchases_arr, category, category_id_arr, result;
    category = _.find(initial_categories, function(category) {
      return category.slug === category_slug;
    });
    all_categories = this.getAllNestedCategories(initial_categories, category_slug);
    all_categories.unshift(category);
    category_id_arr = _.pluck(all_categories, 'id');
    all_purchases_arr = _.pluck(initial_categories, "category_purchase");
    all_purchases = _.flatten(all_purchases_arr, true);
    all_catalogs_arr = _.pluck(all_purchases, "catalogs");
    all_catalogs = _.flatten(all_catalogs_arr, true);
    result = _.map(category_id_arr, function(id) {
      return _.filter(all_catalogs, function(catalog) {
        return _.some(catalog.categories, function(category_id) {
          return category_id === id;
        });
      });
    });
    return this.unique(_.flatten(result, true));
  },
  convertCatalogsToFlatProducts: function(catalogs) {
    var new_products_arr;
    new_products_arr = _.pluck(catalogs, 'product_catalog');
    return _.flatten(new_products_arr, true);
  },
  convertPurchasesToFlatProducts: function(collection) {
    var tmp_collection;
    tmp_collection = [];
    if (collection.length > 0) {
      collection.forEach(function(purchase) {
        return purchase.catalogs.forEach(function(catalog) {
          return catalog.product_catalog.forEach(function(product) {
            product.cpp_catalog = catalog.cpp_catalog;
            return tmp_collection.push(product);
          });
        });
      });
    }
    return tmp_collection;
  },
  unique: function(arr) {
    var arr_id;
    arr_id = _.uniq(_.pluck(arr, 'id'));
    return _.map(arr_id, function(id) {
      return _.find(arr, function(el) {
        return el.id === id;
      });
    });
  },
  unionProductCollections: function(collection1, collection2) {
    var c1, c2, index_arr, union;
    c1 = _.pluck(collection1, 'id');
    c2 = _.pluck(collection2, 'id');
    index_arr = _.intersection(c1, c2);
    union = _.union(collection1, collection2);
    return _.map(index_arr, function(id) {
      return _.find(union, function() {
        return prod(prod.id === id);
      });
    });
  },
  chackProperties: function(cpp_properties, product_properties) {
    var properties_filled, values_str;
    properties_filled = _.every(cpp_properties, function(property) {
      return property.value !== void 0;
    });
    if (properties_filled) {
      values_str = _.pluck(cpp_properties, 'value').join(',');
      if (_.contains(product_properties.split(''), values_str)) {
        $.snackbar({
          timeout: 5000,
          content: 'Товары с данными характеристиками найдены'
        });
        return true;
      } else {
        $.snackbar({
          timeout: 5000,
          content: 'Нет товара с такими характеристиками, пожалуйста, попробуйте другие варианты'
        });
        return false;
      }
    }
  },
  getCategorySlug: function() {
    var current_category_slug, parse_url, url;
    url = $(location).attr('pathname');
    parse_url = url.split('/')[1];
    current_category_slug = parse_url.slice(9);
    if (url.split('/')[1] === 'purchases') {
      current_category_slug = 'purchase';
    }
    return current_category_slug;
  },
  getPurchaseIdByUrl: function() {
    var url;
    url = $(location).attr('pathname');
    return url.split('/')[2];
  }
};

module.exports = Methods;
