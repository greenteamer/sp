var gulp = require('gulp'),
		concatCss = require('gulp-concat-css'),
		minifyCss = require('gulp-minify-css'),
		rename = require("gulp-rename"),
		cjsx = require('gulp-cjsx'),
		uglify = require('gulp-uglify'),
		source = require('vinyl-source-stream'),
		browserify = require('browserify'),
		reactify = require('reactify'),
		coffeeReactify = require('coffee-reactify'),
		watchify = require('watchify'),
		gutil = require('gutil'),
		streamify = require('gulp-streamify');


// gulp for css
gulp.task('default', function(){
	gulp.src('css/test/*.css')
		.pipe(concatCss('bundle.css'))
		.pipe(minifyCss())
		.pipe(rename('bundle.min.css'))
		.pipe(gulp.dest('css/'));
});

gulp.task('watch-css', function(){
	gulp.watch('css/test/*.css', ['default']);
});


// переменная path - настройки констант для путей и названий файлов
// 4 таска для билдинга 4 файлов для главной страницы, категорий, товаров и закупок
// последний таск запускает их все
// Умеет работать с COFFEESCRIPT
var path = {
	DEST: 'client',
	DEST_BUILD: 'client/build',
	PROD_DEST_BUILD: 'client/build/production',
	DEST_SRC: 'client/dev',
	index: {
		MINIFIED_OUT: 'index-build.min.js',
		OUT: 'index-build.js',
		ENTRY_POINT: './client/dev/index/main.jsx'
	},
	category: {
		MINIFIED_OUT: 'category-build.min.js',
		OUT: 'category-build.js',
		ENTRY_POINT: './client/dev/category/main.jsx'
	},
	product: {
		MINIFIED_OUT: 'product-build.min.js',
		OUT: 'product-build.js',
		ENTRY_POINT: './client/dev/product/main.jsx'
	},
	purchase: {
		MINIFIED_OUT: 'purchase-build.min.js',
		OUT: 'purchase-build.js',
		ENTRY_POINT: './client/dev/purchase/main.jsx'
	}
}


// PRODUCTION
// собираем файлы для продакшена
gulp.task('index-build', function(){
  browserify({
    entries: [path.index.ENTRY_POINT],
    transform: [coffeeReactify],
  })
    .bundle()
    .pipe(source(path.index.MINIFIED_OUT))
    .pipe(streamify(uglify({sequences: true})))
    .pipe(gulp.dest(path.PROD_DEST_BUILD))
});


gulp.task('category-build', function(){
  browserify({
    entries: [path.category.ENTRY_POINT],
    transform: [coffeeReactify],
  })
    .bundle()
    .pipe(source(path.category.MINIFIED_OUT))
    .pipe(streamify(uglify({sequences: true})))
    .pipe(gulp.dest(path.PROD_DEST_BUILD))
});


gulp.task('product-build', function(){
  browserify({
    entries: [path.product.ENTRY_POINT],
    transform: [coffeeReactify],
  })
    .bundle()
    .pipe(source(path.product.MINIFIED_OUT))
    .pipe(streamify(uglify({sequences: true})))
    .pipe(gulp.dest(path.PROD_DEST_BUILD))
});


gulp.task('purchase-build', function(){
  browserify({
    entries: [path.purchase.ENTRY_POINT],
    transform: [coffeeReactify],
  })
    .bundle()
    .pipe(source(path.purchase.MINIFIED_OUT))
    .pipe(streamify(uglify({sequences: true})))
    .pipe(gulp.dest(path.PROD_DEST_BUILD))
});


// WATCH COFFEE-SCRIPT
// WATCH COFFEE-SCRIPT
// WATCH COFFEE-SCRIPT
gulp.task('coffee-index-watch', function(){
	var watcher = watchify(browserify({
		entries: ['./client/dev/index/main.cjsx'],
		transform: [coffeeReactify],
		debug: true,
		cache:{}, packageCache: {}, fullPath: true
	}));

	return watcher.on('update', function(){
		watcher.bundle()
			.pipe(source(path.index.OUT))
			.pipe(gulp.dest('client/build/dev_cjsx'))
		console.log('coffee index-watch Update');
	})
		.bundle()
		.pipe(source(path.index.OUT))
		.pipe(gulp.dest('client/build/dev_cjsx'))
});


gulp.task('coffee-category-watch', function(){
	var watcher = watchify(browserify({
		entries: ['./client/dev/category/main.jsx'],
		transform: [coffeeReactify],
		debug: true,
		cache:{}, packageCache: {}, fullPath: true
	}));

	return watcher.on('update', function(){
		watcher.bundle()
			.pipe(source(path.category.OUT))
			.pipe(gulp.dest('client/build/dev_cjsx'))
			console.log('category-watch Update');
	})
		.bundle()
		.pipe(source(path.category.OUT))
		.pipe(gulp.dest('client/build/dev_cjsx'))
});

gulp.task('coffee-product-watch', function(){
	var watcher = watchify(browserify({
		entries: ['./client/dev/product/main.jsx'],
		transform: [coffeeReactify],
		debug: true,
		cache:{}, packageCache: {}, fullPath: true
	}));

	return watcher.on('update', function(){
		watcher.bundle()
			.pipe(source(path.product.OUT))
			.pipe(gulp.dest('client/build/dev_cjsx'))
			console.log('product-watch Update');
	})
		.bundle()
		.pipe(source(path.product.OUT))
		.pipe(gulp.dest('client/build/dev_cjsx'))
});

gulp.task('coffee-purchase-watch', function(){
	var watcher = watchify(browserify({
		entries: ['./client/dev/purchase/main.jsx'],
		transform: [coffeeReactify],
		debug: true,
		cache:{}, packageCache: {}, fullPath: true
	}));

	return watcher.on('update', function(){
		watcher.bundle()
			.pipe(source(path.purchase.OUT))
			.pipe(gulp.dest('client/build/dev_cjsx'))
			console.log('purchase-watch Update');
	})
		.bundle()
		.pipe(source(path.purchase.OUT))
		.pipe(gulp.dest('client/build/dev_cjsx'))
});


gulp.task('coffee', ['coffee-index-watch', 'coffee-category-watch', 'coffee-product-watch', 'coffee-purchase-watch']);
gulp.task('default', ['index-watch', 'category-watch', 'product-watch', 'purchase-watch']);
gulp.task('production', ['index-build', 'category-build', 'product-build', 'purchase-build']);
