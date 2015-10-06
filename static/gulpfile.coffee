gulp = require 'gulp'
concatCss = require 'gulp-concat-css'
minifyCss = require 'gulp-minify-css'
rename = require 'gulp-rename'
cjsx = require 'gulp-cjsx'
uglify = require 'gulp-uglify'
source = require 'vinyl-source-stream'
browserify = require 'browserify'
reactify = require 'reactify'
coffeeReactify = require 'coffee-reactify'
watchify = require 'watchify'
gutil = require 'gutil'
streamify = require 'gulp-streamify'


# gulp for css
gulp.task 'default', ->
	gulp.src('css/test/*.css').pipe(concatCss('bundle.css')).pipe(minifyCss()).pipe(rename('bundle.min.css')).pipe gulp.dest('css/')
	return
gulp.task 'watch-css', ->
	gulp.watch 'css/test/*.css', [ 'default' ]
	return


# переменная path - настройки констант для путей и названий файлов
# 4 таска для билдинга 4 файлов для главной страницы, категорий, товаров и закупок
# последний таск запускает их все
# Умеет работать с COFFEESCRIPT
path =
	DEST: 'client'
	DEST_BUILD: 'client/build/dev_cjsx'
	PROD_DEST_BUILD: 'client/build/production'
	DEST_SRC: 'client/dev'
	index:
		MINIFIED_OUT: 'index-build.min.js'
		OUT: 'index-build.js'
		ENTRY_POINT: './client/dev/index/main.cjsx'
	category:
		MINIFIED_OUT: 'category-build.min.js'
		OUT: 'category-build.js'
		ENTRY_POINT: './client/dev/category/main.jsx'
	product:
		MINIFIED_OUT: 'product-build.min.js'
		OUT: 'product-build.js'
		ENTRY_POINT: './client/dev/product/main.jsx'
	purchase:
		MINIFIED_OUT: 'purchase-build.min.js'
		OUT: 'purchase-build.js'
		ENTRY_POINT: './client/dev/purchase/main.jsx'


# PRODUCTION
# собираем файлы для продакшена
gulp.task 'index-build', ->
	browserify
		entries: [ path.index.ENTRY_POINT ]
		transform: [ coffeeReactify ]
	.bundle()
	.pipe source(path.index.MINIFIED_OUT)
	.pipe streamify(uglify(sequences: true))
	.pipe gulp.dest(path.PROD_DEST_BUILD)
	return

gulp.task 'category-build', ->
	browserify(
		entries: [ path.category.ENTRY_POINT ]
		transform: [ coffeeReactify ])
	.bundle()
	.pipe source(path.category.MINIFIED_OUT)
	.pipe streamify(uglify(sequences: true))
	.pipe gulp.dest(path.PROD_DEST_BUILD)
	return

gulp.task 'product-build', ->
	browserify(
		entries: [ path.product.ENTRY_POINT ]
		transform: [ coffeeReactify ])
	.bundle()
	.pipe source(path.product.MINIFIED_OUT)
	.pipe streamify(uglify(sequences: true))
	.pipe gulp.dest(path.PROD_DEST_BUILD)
	return

gulp.task 'purchase-build', ->
	browserify(
		entries: [ path.purchase.ENTRY_POINT ]
		transform: [ coffeeReactify ])
	.bundle()
	.pipe source(path.purchase.MINIFIED_OUT)
	.pipe streamify(uglify(sequences: true))
	.pipe gulp.dest(path.PROD_DEST_BUILD)
	return


# WATCH COFFEE-SCRIPT
# WATCH COFFEE-SCRIPT
# WATCH COFFEE-SCRIPT
gulp.task 'coffee-index-watch', ->
	watcher = watchify(browserify(
  		entries: [ path.index.ENTRY_POINT ]
  		transform: [ coffeeReactify ]
  		debug: true
  		cache: {}
  		packageCache: {}
  		fullPath: true))
	watcher.on('update', ->
		watcher
      .bundle()
      .pipe source(path.index.OUT)
      .pipe gulp.dest(path.DEST_BUILD)
		console.log 'coffee index-watch Update')
    .bundle()
    .pipe source(path.index.OUT)
    .pipe gulp.dest(path.DEST_BUILD)

gulp.task 'coffee-category-watch', ->
	watcher = watchify(browserify(
		entries: [ path.category.ENTRY_POINT ]
		transform: [ coffeeReactify ]
		debug: true
		cache: {}
		packageCache: {}
		fullPath: true))
	watcher.on('update', ->
		watcher
      .bundle()
      .pipe source(path.category.OUT)
      .pipe gulp.dest(path.DEST_BUILD)
		console.log 'category-watch Update')
    .bundle()
    .pipe source(path.category.OUT)
    .pipe gulp.dest(path.DEST_BUILD)

gulp.task 'coffee-product-watch', ->
	watcher = watchify(browserify(
		entries: [ path.product.ENTRY_POINT ]
		transform: [ coffeeReactify ]
		debug: true
		cache: {}
		packageCache: {}
		fullPath: true))
	watcher.on('update', ->
		watcher
      .bundle()
      .pipe source(path.product.OUT)
      .pipe gulp.dest(path.DEST_BUILD)
		console.log 'product-watch Update')
    .bundle()
    .pipe source(path.product.OUT)
    .pipe gulp.dest(path.DEST_BUILD)

gulp.task 'coffee-purchase-watch', ->
	watcher = watchify(browserify(
		entries: [ path.purchase.ENTRY_POINT ]
		transform: [ coffeeReactify ]
		debug: true
		cache: {}
		packageCache: {}
		fullPath: true))
	watcher.on('update', ->
		watcher
      .bundle()
      .pipe source(path.purchase.OUT)
      .pipe gulp.dest(path.DEST_BUILD)
		console.log 'purchase-watch Update')
    .bundle()
    .pipe source(path.purchase.OUT)
    .pipe gulp.dest(path.DEST_BUILD)

gulp.task 'default', [
	'index-watch'
	'category-watch'
	'product-watch'
	'purchase-watch'
]
gulp.task 'production', [
	'index-build'
	'category-build'
	'product-build'
	'purchase-build'
]

gulp.task 'coffee', [
	'coffee-index-watch'
	'coffee-category-watch'
	'coffee-product-watch'
	'coffee-purchase-watch'
]
