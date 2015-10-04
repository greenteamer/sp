// переменная path - настройки констант для путей и названий файлов
// 4 таска для билдинга 4 файлов для главной страницы, категорий, товаров и закупок
// последний таск запускает их все
var gulp = require('gulp'),
		concatCss = require('gulp-concat-css'),
		minifyCss = require('gulp-minify-css'),
		rename = require("gulp-rename"),
		uglify = require('gulp-uglify'),
		source = require('vinyl-source-stream'),
		browserify = require('browserify'),
		reactify = require('reactify'),
		watchify = require('watchify'),
		streamify = require('gulp-streamify');


var path = {
	MINIFIED_OUT: 'build.min.js',
	DEST: 'client',
	DEST_BUILD: 'client/build',
	DEST_SRC: 'client/dev',
	index: {
		OUT: 'index-build.js',
		ENTRY_POINT: './client/dev/index/main.jsx'
	},
	category: {
		OUT: 'category-build.js',
		ENTRY_POINT: './client/dev/category/main.jsx'
	},
	product: {
		OUT: 'product-build.js',
		ENTRY_POINT: './client/dev/product/main.jsx'	
	},
	purchase: {
		OUT: 'purchase-build.js',
		ENTRY_POINT: './client/dev/purchase/main.jsx'
	}	
}


//таск для index файла
gulp.task('index-watch', function(){
	var watcher = watchify(browserify({
		entries: [path.index.ENTRY_POINT],
		transform: [reactify],
		debug: true,
		cache:{}, packageCache: {}, fullPath: true
	}));

	return watcher.on('update', function(){
		watcher.bundle()
			.pipe(source(path.index.OUT))
			.pipe(gulp.dest(path.DEST_BUILD))
			console.log('index-watch Update');
	})
		.bundle()
		.pipe(source(path.index.OUT))
		.pipe(gulp.dest(path.DEST_BUILD))
});


//таск для category файла
gulp.task('category-watch', function(){
	var watcher = watchify(browserify({
		entries: [path.category.ENTRY_POINT],
		transform: [reactify],
		debug: true,
		cache:{}, packageCache: {}, fullPath: true
	}));

	return watcher.on('update', function(){
		watcher.bundle()
			.pipe(source(path.category.OUT))
			.pipe(gulp.dest(path.DEST_BUILD))
			console.log('category-watch Update');
	})
		.bundle()
		.pipe(source(path.category.OUT))
		.pipe(gulp.dest(path.DEST_BUILD))
});


//таск для product файла
gulp.task('product-watch', function(){
	var watcher = watchify(browserify({
		entries: [path.product.ENTRY_POINT],
		transform: [reactify],
		debug: true,
		cache:{}, packageCache: {}, fullPath: true
	}));

	return watcher.on('update', function(){
		watcher.bundle()
			.pipe(source(path.product.OUT))
			.pipe(gulp.dest(path.DEST_BUILD))
			console.log('product-watch Update');
	})
		.bundle()
		.pipe(source(path.product.OUT))
		.pipe(gulp.dest(path.DEST_BUILD))
});


//таск для product файла
gulp.task('purchase-watch', function(){
	var watcher = watchify(browserify({
		entries: [path.purchase.ENTRY_POINT],
		transform: [reactify],
		debug: true,
		cache:{}, packageCache: {}, fullPath: true
	}));

	return watcher.on('update', function(){
		watcher.bundle()
			.pipe(source(path.purchase.OUT))
			.pipe(gulp.dest(path.DEST_BUILD))
			console.log('purchase-watch Update');
	})
		.bundle()
		.pipe(source(path.purchase.OUT))
		.pipe(gulp.dest(path.DEST_BUILD))
});


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


gulp.task('default', ['index-watch', 'category-watch', 'product-watch', 'purchase-watch']);




